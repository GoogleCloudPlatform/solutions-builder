"""
Rule object in the ORM
"""

import os
from common.models import BaseModel
from fireo.fields import IDField, TextField, ListField, BooleanField, NumberField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


class Rule(BaseModel):
  """Rule ORM class
  """
  name = TextField()
  id = IDField(required=True)
  fields = ListField()
  aggregation_type = TextField()
  count_columns = ListField()
  is_enabled = BooleanField()
  threshold = NumberField()
  base_weight = NumberField()
  incremental_weight = NumberField()
  output_columns = ListField()
  sql_query = TextField()
  flag_condition = TextField()
  remark = TextField()
  comments = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "rules"
