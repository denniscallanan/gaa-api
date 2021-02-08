from datetime import date
from typing import Optional

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


class Player(DTO):
    caps: Optional[int]
    career_end: Optional[date]
    career_start: Optional[date]
    dob: Optional[date]
    full_name: Optional[str]
    team_id: Optional[str]
    typical_position: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["full_name", "team_id"]

    @classmethod
    def get_uneditable_fields(cls):
        return ["full_name"]


class PlayerResponseModel(ResponseModel):
    result: Player.get_identified_record()
