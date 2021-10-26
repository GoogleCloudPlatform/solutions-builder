""" Claim endpoints """
import csv
import codecs
import datetime
import json
from io import StringIO
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.concurrency import run_in_threadpool
from schemas.claim import ClaimModel, GcsBucketInfoModel
from google.cloud import storage
from common.models import Claim
from common.utils.stream_to_bq import stream_claim_to_bigquery, delete_claim_in_bigquery
from common.utils.logging_handler import Logger
from common.db_client import bq_client
from common.utils.neo4j_new_incoming_claim import create_claim_neo4j, update_claim_neo4j, delete_claim_neo4j
# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/claim", tags=["Claim"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/{claim_id}", response_model=ClaimModel)
async def get_claim(claim_id: str):
  """Get a claim

  Args:
    claim_id (str): unique id of the claim

  Raises:
    HTTPException: 404 Not Found if claim doesn't exist for the given claim id
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [claim]: Claim object for the provided claim id
  """
  claim = await run_in_threadpool(Claim.find_by_claim_id, claim_id)
  if claim is None:
    raise HTTPException(status_code=404, detail="Claim not found")
  return claim


@router.post("")
async def create_claim(input_claim: ClaimModel):
  """Register a Claim

  Args:
    input_claim (ClaimModel): Required body of the claim

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: Claim ID of the claim if the claim is successfully created,
    {'status': 'Failed'} if the claim creation raises an exception
  """
  try:
    claim = await run_in_threadpool(Claim.find_by_claim_id,
                                    input_claim.claim_id)
    new_claim = Claim()
    input_claim_dict = {**input_claim.dict()}
    new_claim = new_claim.from_dict(input_claim_dict)

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    client = bq_client()
    if claim is None:
      new_claim.created_timestamp = timestamp
      new_claim.last_updated_timestamp = timestamp
      await run_in_threadpool(new_claim.save)
      await run_in_threadpool(stream_claim_to_bigquery, client,
                              input_claim_dict, "CREATE", timestamp)
      try:
        create_claim_neo4j(input_claim_dict)
      except Exception as e:
        Logger.error(e)
    else:
      new_claim.last_updated_timestamp = timestamp
      await run_in_threadpool(new_claim.update, claim.id)
      await run_in_threadpool(stream_claim_to_bigquery, client,
                              input_claim_dict, "UPDATE", timestamp)
      try:
        update_claim_neo4j(input_claim_dict)
      except Exception as e:
        Logger.error(e)
    return new_claim.claim_id
  except Exception as e:
    raise HTTPException(status_code=500, detail=e) from e


@router.put("")
async def update_claim(input_claim: ClaimModel):
  """Update a claim

  Args:
    input_claim (ClaimModel): Required body of the claim

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the claim is updated,
    {'status': 'Failed'} if the claim updation raises an exception
  """
  claim = Claim()
  input_claim_dict = {**input_claim.dict()}
  claim = claim.from_dict(input_claim_dict)
  existing_claim = Claim.find_by_claim_id(input_claim_dict["claim_id"])

  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

  if existing_claim:
    try:
      claim.last_updated_timestamp = timestamp
      client = bq_client()
      await run_in_threadpool(claim.update, existing_claim.id)
      await run_in_threadpool(stream_claim_to_bigquery, client,
                              input_claim_dict, "UPDATE", timestamp)
      try:
        update_claim_neo4j(input_claim_dict)
      except Exception as e:
        Logger.error(e)
    except Exception as e:
      raise HTTPException(status_code=500, detail=FAILED_RESPONSE) from e
  else:
    raise HTTPException(status_code=404, detail="Claim not found")

  return SUCCESS_RESPONSE


@router.delete("/{claim_id}")
async def delete_claim(claim_id: str):
  """Delete a claim

  Args:
    claim_id (str): unique id of the claim

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    [JSON]: {'status': 'Succeed'} if the claim is deleted,
    {'status': 'Failed'} if the claim deletion raises an exception
  """
  claim = await run_in_threadpool(Claim.find_by_claim_id, claim_id)
  if claim is None:
    raise HTTPException(status_code=404, detail="Claim not found")
  await run_in_threadpool(Claim.collection.delete, claim.key)
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
  client = bq_client()
  await run_in_threadpool(delete_claim_in_bigquery, client, claim_id, timestamp)
  try:
    delete_claim_neo4j(claim.__dict__)
  except Exception as e:
    Logger.error(e)
  return SUCCESS_RESPONSE


@router.post("/upload_bulk_claim", response_model=str)
async def bulk_create_claim(claim_csv_file: UploadFile = File(...)):
  """Upload Claims in bulk using CSV file

  Args:
    claim_csv_file (UploadFile): Upload CSV file consisting of claims
    The column header names in csv should match the object name in post API

  Returns:
    [List]: List of claim id of the claims created
  """
  csv_reader = csv.DictReader(
      codecs.iterdecode(claim_csv_file.file, "utf-8"), delimiter=",")
  json_array = []
  for row in csv_reader:
    json_array.append(row)

  claim_id_list = await bulk_insert_claims_list(json_array)

  return f"Uploaded {len(claim_id_list)} claims"


@router.post("/upload_bulk_claim_gcs", response_model=str)
async def bulk_gcs_bucket_claim_file(file_info: GcsBucketInfoModel):
  """Upload Claims in bulk using CSV file present in Gcs storage

  Args:
    file_info (dict):
      bucket_name (str): Gcs storage bucket name.
      file_name (str): CSV file name with extension
    The column header names in csv should match the object name in post API

  Returns:
    [List]: List of claim id of the claims created
  """
  storage_client = storage.Client()
  bucket_name = file_info.bucket_name
  file_name = file_info.file_name

  # get bucket with name
  bucket = storage_client.bucket(bucket_name)

  try:
    # get bucket data as blob
    blob = bucket.get_blob(file_name)
    if not blob:
      raise HTTPException(
          status_code=404,
          detail="The specified file or bucket does not exist or don't have " +
          "sufficient permissions.")
  except Exception as e:
    raise e

  # download file as bytes
  file_data = blob.download_as_bytes()
  byte_content = file_data
  content = byte_content.decode()
  file = StringIO(content)

  csv_reader = csv.DictReader(file, delimiter=",")

  json_array = []
  for row in csv_reader:
    json_array.append(row)

  claim_id_list = await bulk_insert_claims_list(json_array)

  return f"Uploaded {len(claim_id_list)} claims"


async def bulk_insert_claims_list(claims_list):
  claim_id_list = []
  for claim_object in claims_list:
    claim_object = dict(claim_object)
    claim_object["document_details"] = json.loads(
        claim_object["document_details"])
    claim = Claim()
    claim = claim.from_dict(claim_object)
    await run_in_threadpool(claim.save)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    client = bq_client()
    await run_in_threadpool(stream_claim_to_bigquery, client, claim_object,
                            "CREATE", timestamp)
    try:
      create_claim_neo4j(claim_object)
    except Exception as e:
      Logger.error(e)
    claim_id_list.append(claim.claim_id)
  return claim_id_list
