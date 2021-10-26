"""
  Endpoints related to risk_profile
"""
import requests
from asyncio import gather
from fastapi import APIRouter, Response, status
from fastapi.exceptions import HTTPException
from fastapi.concurrency import run_in_threadpool
from common.models import Claim
from schemas.risk_profile_schema import RiskProfileClaim, extra_response_codes

router = APIRouter(tags=["Risk Profile"])


@router.get(
    "/risk_profile/{claim_id}",
    response_model=RiskProfileClaim,
    responses=extra_response_codes)
async def risk_profile(claim_id: str, response: Response):  # pylint: disable=unused-argument
  """Returns the rules engine score

  Args:
      claim_id (str): Claim id of the claim

  Returns:
      RiskProfileClaim: Fields that consist of rules engine score
      and similarity engine
  """
  re_url = "http://rules-engine/rules_engine/v1/get_risk_profile/"
  se_url = "http://similarity-engine/similarity_engine/v1/similarity_profile/"

  claim = await run_in_threadpool(Claim.find_by_claim_id, claim_id)
  if claim is None:
    raise HTTPException(status_code=404, detail="Claim not found")
  else:

    api_res = await gather(
        run_in_threadpool(requests.get, f"{re_url}{claim_id}"),
        run_in_threadpool(requests.get, f"{se_url}{claim_id}")
    )
    res_re, res_se = api_res

    result = {}
    if res_re.status_code == 200 and res_se.status_code == 200:
      result = res_re.json()
      result["similarity_claim_list"] = res_se.json()
      result["rules_engine_status"] = "Success"
      result["similarity_engine_status"] = "Success"
      return result
    elif res_re.status_code == 204:
      response.status_code = status.HTTP_204_NO_CONTENT
      return response
    elif res_re.status_code == 200 and res_se.status_code == 500:
      result = res_re.json()
      result["similarity_claim_list"] = []
      result["rules_engine_status"] = "Success"
      result["similarity_engine_status"] = f"Failed: {res_se.text}"
      return result
    elif res_re.status_code == 500:
      raise HTTPException(
          status_code=500,
          detail=f"Unable to parse risk profile response: {res_re.text}")
    else:
      raise ValueError(f"Unable to parse risk profile \
        response: {res_re.text} {res_se.text}")
