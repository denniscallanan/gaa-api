from datetime import date
from typing import Optional

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class TeamManagerTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("PLAY"))
    position_end = DateField(null=True)
    position_start = DateField(null=True)
    team_id = CharField()
    dob = DateField(null=True)
    full_name = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'team_manager'
        primary_key = CompositeKey('id_tag', 'version_num')


class TeamManager(DTO):
    position_end: Optional[date]
    position_start: Optional[date]
    team_id: Optional[str]
    dob: Optional[date]
    full_name: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["full_name", "team_id"]

    @classmethod
    def get_uneditable_fields(cls):
        return ["full_name", "team_id"]


class TeamManagerResponseModel(ResponseModel):
    result: TeamManager.get_identified_record()
