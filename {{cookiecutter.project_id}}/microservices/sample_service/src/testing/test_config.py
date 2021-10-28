"""Static Values for Testing"""
import os

CLAIM_ID = "U2DDBkl3Ayg0PWudzhIi"

TEST_INPUT_CLAIM = {
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
    "EWA_DocType_1": {
      "_uri": "gs://bv-erap-tf/sample-documents/nycdlfull.pdf",
      "_created_on": "2012-04-23T18:25:43.511Z",
      "document_quality_score": 0.72,
      "id_number_back": "OCT335WQ11",
      "address": "2345 ANYWHERE STREET ALBANY, NY 12222",
      "gender": "M",
      "height": "6'-00\"",
      "name": "MICHAEL MATTHEW MOTORIST",
      "dob": "1988-03-16",
      "expiration_date": "1988-03-16",
      "issue_date": "1988-03-16",
      "id_number": "123456789",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_2": {
      "_uri": "gs://bv-erap-tf/sample-documents/Samplepassport.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.03,
      "date_of_birth": "2021-06-16",
      "document_id": "585468609",
      "expiration_date": "2021-06-16",
      "family_name": "GOLDBECK",
      "given_names": "ETHAN RAY",
      "issue_date": "2021-06-16",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_3" : {
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
    "EWA_DocType_4": {
      "_uri": "gs://bv-erap-tf/sample-documents/sample-fp-1.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.0,
      "name": "VCHENKO, DARYNA",
      "dob": "2021-06-16",
      "expire_date": "2021-06-16",
      "gender": "F",
      "origin_country": "UKR",
      "passport_number": "X0000000<",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_5": {
      "_uri": "gs://bv-erap-tf/sample-documents/sample-fp-1.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.0,
      "name": "VCHENKO, DARYNA",
      "dob": "2021-06-16",
      "expire_date": "2021-06-16",
      "gender": "F",
      "id_number": "484782",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_15": {
      "_uri": "gs://bv-erap-tf/sample-documents/sample-recid-2.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.83,
      "id_number": "484782",
      "name": "Rue McClanahan",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_13" : {
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
    "EWA_DocType_14": {
      "_uri": "/sample-documents/Filled Out NYS OCA -- Judment of Divorce.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.92,
      "social_security_no": "122345678",
      "present_hon": "Aaron Judge",
      "index_no": "1005",
      "county": "Ulster",
      "date": "July 5th 2007",
      "calendar_no": "298",
      "defendant": "Sally Mae",
      "plaintiff": "Mike Jones",
      "ias_part": "25",
      "plaintiff_address": "11234 Fake St, Woodstock New York 12498",
      "defendant_address": "987 Main Blvd, Hudson, New York 12983 and",
      "plaintiff_ssn": "876321234",
      "defendant_ssn": "98712224",
      "entity_extraction_score": 1.0
    },
    "EWA_DocType_16":{
      "_uri": "gs://bv-erap-tf/sample-documents/sample-transcript-3.pdf",
      "_created_on": "2021-06-16",
      "document_quality_score": 0.95,
      "name": "Knox, Ozetta M.",
      "school": "UNIVERSITY OF ILLINOIS AT SPRINGFIELD",
      "dob": "20-Jul-xxxx",
      "date": "2021-06-16",
      "address": "SPRINGFIELD, IL 62703-5407",
      "entity_extraction_score": 1.0
    }
  }
}

TEST_COMPLETE_CLAIM = {
    "claim_id": "U2DDBkl3Ayg0PWudzhIi",
    "first_name": "John",
    "middle_name": "A",
    "last_name": "Marshal",
    "date_of_birth": "1994-09-10",
    "tax_payer_id": "ABHNMK",
    "mail_address_line1": "342#",
    "mail_address_line2": "Nicholson Road",
    "mail_address_city": "Sydney",
    "mail_address_state": "NSW",
    "mail_address_zipcode": "133001",
    "res_address_line1": "342#",
    "res_address_line2": "Nicholson Road",
    "res_address_city": "Sydney",
    "res_address_state": "NSW",
    "res_address_zipcode": "133001",
    "email_address": "john.338@gmail.com",
    "phone_num": "9996754321"
}

TESTDATA_FILENAME = os.path.join(
    os.path.dirname(__file__), "..", "testing", "claim_test_file.csv")
