from datetime import date
from typing import Optional, List

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class PlayerTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("PLAY"))
    caps = IntegerField(null=True)
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    team_id = CharField()
    typical_position = CharField(null=True)
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'player'
        primary_key = CompositeKey('id_tag', 'version_num')

    def to_record(self):
        return self.to_model(PlayerRecord)


class EditablePlayer(DTO):
    caps: Optional[int]
    career_end: Optional[date]
    career_start: Optional[date]
    dob: Optional[date]
    typical_position: Optional[str]


class Player(EditablePlayer):
    full_name: str
    team_id: str


class PlayerRecord(Player):
    id_tag: str


class PlayerResponseModel(ResponseModel):
    result: Optional[PlayerRecord]


class PlayerResponseModelList(ResponseModel):
    result: List[PlayerRecord]
