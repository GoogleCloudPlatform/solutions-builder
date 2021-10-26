"""
Claim object in the ORM
"""

import os

import common.config as global_config
from common.db_client import bq_client
from common.models import BaseModel
from common.utils.neo4j_new_incoming_claim import authenticate_neo4j
from fireo.fields import Field, TextField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", os.environ.get("PROJECT_ID", ""))


# sample class
class Claim(BaseModel):
  """Claim ORM class
  """
  claim_id = TextField()
  first_name = TextField()
  middle_name = TextField()
  last_name = TextField()
  date_of_birth = TextField()
  mail_address_line1 = TextField()
  mail_address_line2 = TextField()
  mail_address_city = TextField()
  mail_address_state = TextField()
  mail_address_zipcode = TextField()
  res_address_line1 = TextField()
  res_address_line2 = TextField()
  res_address_city = TextField()
  res_address_state = TextField()
  res_address_zipcode = TextField()
  email_address = TextField()
  phone_num = TextField()
  itin_number = TextField()
  tf_number = TextField()
  dl_number = TextField()
  register_ip_address = TextField()
  document_details = Field()
  created_timestamp = TextField()
  last_updated_timestamp = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "claims"

  # pylint: disable = line-too-long
  @classmethod
  def get_rules_engine_score(cls, claim_id):
    query = f"SELECT * FROM {global_config.PROJECT_ID}.{global_config.DATABASE_PREFIX}rules_engine.final_rules_engine_score WHERE claim_id = \"{claim_id}\""

    client = bq_client()
    query_job = client.query(query)
    results = query_job.result()
    records = [dict(row) for row in results]
    if records != []:
      return records[0]
    else:
      return {}

  # pylint: enable= line-too-long

  @classmethod
  def check_claim_neo4j(cls, claim_id):
    query = f"""MATCH (c:claim)
            WHERE c.claim_id = \"{claim_id}\"
            RETURN c.claim_id as claim_id
            """
    graph = authenticate_neo4j()
    graph_session = graph.session()
    response = graph_session.run(query)
    records = [dict(row) for row in response]
    return records != [] and records[0].get("claim_id")

  @classmethod
  def generate_similarity_response(cls, claim_id):
    query = f"""MATCH (c1:claim) -[x]-(c2:claim)
            WHERE c1.claim_id <> c2.claim_id  and
            c1.processed_flag = "true" and
            c2.processed_flag = "true" and
            c1.claim_id = \"{claim_id}\"
            RETURN c2.claim_id as claim_id, collect(type(x)) as relationship_list
            ORDER BY size(relationship_list) DESC LIMIT 5
            """
    graph = authenticate_neo4j()
    graph_session = graph.session()
    response = graph_session.run(query)
    records = [dict(row) for row in response]
    if records != []:
      return records
    else:
      return []

  @classmethod
  def find_by_claim_id(cls, uuid):
    """Find the claim using claim id(UUID)
    Args:
        uuid (string): Claim ID
    Returns:
        Claim: Claim Object
    """
    return Claim.collection.filter("claim_id", "==", uuid).get()
