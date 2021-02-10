from datetime import date
from typing import Optional, List

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

    def to_record(self):
        return self.to_model(TeamManagerRecord)


class EditableTeamManager(DTO):
    position_end: Optional[date]
    position_start: Optional[date]
    dob: Optional[date]


class TeamManager(EditableTeamManager):
    team_id: str
    full_name: str


class TeamManagerRecord(TeamManager):
    id_tag: str


class TeamManagerResponseModel(ResponseModel):
    result: Optional[TeamManagerRecord]


class TeamManagerResponseModelList(ResponseModel):
    result: List[TeamManagerRecord]
