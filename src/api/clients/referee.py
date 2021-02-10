from datetime import date
from typing import Optional, List

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

    def to_record(self):
        return self.to_model(RefereeRecord)


class EditableReferee(DTO):
    career_end: Optional[date]
    career_start: Optional[date]
    county: Optional[str]
    dob: Optional[date]


class Referee(EditableReferee):
    full_name: str


class RefereeRecord(EditableReferee):
    id_tag: str


class RefereeResponseModel(ResponseModel):
    result: Optional[RefereeRecord]


class RefereeResponseModelList(ResponseModel):
    result: List[RefereeRecord]
