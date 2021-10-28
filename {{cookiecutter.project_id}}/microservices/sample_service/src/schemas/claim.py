"""
Pydantic Model for Claim API's
"""
from typing import Optional
from pydantic import BaseModel

class ClaimModel(BaseModel):
  """Claim Pydantic Model"""
  claim_id: str
  first_name: str
  middle_name: Optional[str] = None
  last_name: str
  date_of_birth: str
  mail_address_line1: str
  mail_address_line2: Optional[str] = None
  mail_address_city: str
  mail_address_state: str
  mail_address_zipcode: str
  res_address_line1: str
  res_address_line2: Optional[str] = None
  res_address_city: str
  res_address_state: str
  res_address_zipcode: str
  email_address: str
  phone_num: str
  itin_number: Optional[str] = None
  tf_number: Optional[str] = None
  dl_number: Optional[str] = None
  register_ip_address: Optional[str] = None
  document_details: Optional[dict] = {}


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
        "claim_id" : "c61d7e3c-22ed-497b-97f5-438334c9d0f8",
        "first_name" : "Tony",
        "middle_name" : "I",
        "last_name" : "Stark",
        "date_of_birth" : "2001-07-16",
        "mail_address_line1" : "1 Avenger Way",
        "mail_address_line2" : "4",
        "mail_address_city" : "Brooklyn",
        "mail_address_state" : "new-york",
        "mail_address_zipcode" : "11201",
        "res_address_line1" : "1 Avenger Way",
        "res_address_line2" : "5",
        "res_address_city" : "New York",
        "res_address_state" : "new-york",
        "res_address_zipcode" : "10007",
        "email_address" : "ironman@stark.com",
        "phone_num" : "5185550001",
        "itin_number" : "123456789",
        "tf_number" : "TF1234567",
        "dl_number" : "null",
        "register_ip_address" : "127.0.0.1",
        "document_details" : {
          "EWA_DocType_9" : {
            "_created_on" : "2012-04-23T18:25:43.511Z",
            "_uri" : "/file/path",
            "document_type" : "nycid",
            "address" : "1628 CABRINI BOULEVARD NEW YORK, NY 10007",
            "dob" : "1988-03-16",
            "expiration_date" : "2021-02-01",
            "gender" : "F",
            "id_number" : "16240123192155",
            "id_number_back" : "12345678901234",
            "name" : "SAMPLE WENDY, S",
            "document_quality_score" : 0.99,
            "entity_extraction_score" : 0.99,
            "ewa_document_id" : "e989a57c-492e-40ce-b732-10efb3359818",
            "ewa_document_status" : "UNVERIFIED",
            "ewa_document_analysis_status" : "success",
            "ewa_correction_reason_id" : "null",
            "ewa_document_type_id" : "9"
          },
          "EWA_DocType_10" : {
            "_created_on" : "2021-06-16",
            "_uri" : "gs://bv-erap-tf/sample-documents/marriage_regis.pdf",
            "date_of_marriage" : "2021-06-15",
            "document_type" : "marriage_certificate",
            "person1" : {
              "address" : "",
              "dob" : "1966-10-28",
              "first_name" : "Ross",
              "name" : "Ross Geller Geller",
              "place_of_birth" : "",
              "premarriage_middle" : "Geller",
              "premarriage_surname" : "Geller"
            },
            "person2" : {
              "address" : "49 Hudson Rd. Livermore, CA 94550",
              "dob" : "1968-05-05",
              "first_name" : "Rachel",
              "name" : "Rachel Green Green",
              "place_of_birth" : "19 Grove Street",
              "premarriage_middle" : "Green",
              "premarriage_surname" : "Green"
            },
            "place_of_marriage" : "Campfire St. Moreno",
            "ewa_document_id" : "b542a997-cfcc-4993-aec8-c413c873ba1e",
            "ewa_document_status" : "NEEDS_CORRECTION",
            "ewa_document_analysis_status" : "success",
            "ewa_correction_reason_id" : "12",
            "ewa_document_type_id" : "10"
          },
          "EWA_DocType_3" : {
            "ewa_document_id" : "763c85c2-479e-4c0e-b1c3-abde847cebbf",
            "ewa_document_status" : "NEEDS_CORRECTION",
            "ewa_document_analysis_status" : "success",
            "ewa_correction_reason_id" : "3",
            "ewa_document_type_id" : "3"
          }
        }
      }
    }


class GcsBucketInfoModel(BaseModel):
  """Gcs Bucket blob Pydantic Model"""
  bucket_name: str
  file_name: str

  class Config():
    schema_extra = {
        "example": {
            "bucket_name": "client-claims-data",
            "file_name": "all-claims.csv"
        }
    }
