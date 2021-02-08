from datetime import date
from typing import Optional

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class RefereeTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("PLAY"))
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    county = CharField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'referee'
        primary_key = CompositeKey('id_tag', 'version_num')


class Referee(DTO):
    career_end: Optional[date]
    career_start: Optional[date]
    county: Optional[str]
    dob: Optional[date]
    full_name: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["full_name"]

    @classmethod
    def get_uneditable_fields(cls):
        return ["full_name"]


class RefereeResponseModel(ResponseModel):
    result: Optional[Referee.get_identified_record()]
