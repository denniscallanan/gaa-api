from datetime import date
from typing import Optional

from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel, BaseClient
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class Player(BaseDataModel):
    caps = IntegerField(null=True)
    career_end = DateField(null=True)
    career_start = DateField(null=True)
    dob = DateField(null=True)
    full_name = CharField()
    player_id = AutoField()
    team_id = IntegerField()
    typical_position = CharField(null=True)

    class Meta:
        table_name = 'player'


class PlayerResponse(BaseModel):
    caps: Optional[int]
    career_end: Optional[date]
    career_start: Optional[date]
    dob: Optional[date]
    full_name: str
    player_id: int
    team_id: int
    typical_position: Optional[str]


class PlayerResponseModel(ResponseModel):
    result: PlayerResponse


class PlayerClient(BaseClient):

    def db_model_to_response(self, db_model) -> PlayerResponse:
        return PlayerResponse(**self._get_field_args(db_model))

    @generic_error_wrapper
    def get_player(self, player_id):
        player = Player.get_by_id(player_id)
        response = self.db_model_to_response(player)
        return self.to_response_model(response)
