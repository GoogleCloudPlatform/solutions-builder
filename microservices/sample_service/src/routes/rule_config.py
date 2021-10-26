"""
  Endpoints related to rules configuration
"""
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from schemas.rule_config_schema import PostRuleConfigIn, PostRuleConfigOut, GetRuleConfigOut
from common.models import Rule

router = APIRouter(tags=["Rule Config"])


@router.get("/rule_config/{rule_id}", response_model=GetRuleConfigOut)
async def get_rule_config(rule_id: str):
  """This endpoint will return the data related to rule_id
     from firestore Rule collection

  Args:
      rule_id: Type string

  Raises:
      HTTPException: Type 404 when unknown rule_id is passed

  Returns:
      Response of schema type: GetRuleConfigOut
  """

  data = await run_in_threadpool(Rule.find_by_id, rule_id)
  if data:
    response = {
        "rule_name": data.name,
        "base_weight": data.base_weight,
        "incremental_weight": data.incremental_weight,
        "threshold": data.threshold,
        "is_enabled": data.is_enabled,
    }
  else:
    raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")
  return response


@router.post("/rule_config", response_model=PostRuleConfigOut)
async def post_rule_config(request_body: PostRuleConfigIn):
  """This endpoint will update the data of rule in firestore Rule collection

  Raises:
      HTTPException: Type 404 when unknown rule_id is passed
      HTTPException: Type 500 when unable to update data in firestore

  Returns:
      Response of schema type: PostRuleConfigOut
  """

  data = await run_in_threadpool(Rule.find_by_id, request_body.rule_id)
  if data:
    rule = Rule()
    rule.name = request_body.rule_name
    rule.base_weight = request_body.base_weight
    rule.incremental_weight = request_body.incremental_weight
    rule.threshold = request_body.threshold
    rule.is_enabled = request_body.is_enabled
    try:
      await run_in_threadpool(rule.update, request_body.rule_id)
      return {"rule_id": request_body.rule_id}
    except Exception as exception:
      raise HTTPException(status_code=500, detail=exception) from exception
  else:
    raise HTTPException(status_code=404, detail="unknown data")
