from datetime import date
from typing import Optional, List

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class MatchTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("MATCH"))
    away_team_goals = IntegerField(default=0)
    away_team_id = CharField()
    away_team_manager_id = CharField()
    home_team_manager_id = CharField()
    away_team_points = IntegerField(default=0)
    championship_id = CharField()
    championship_round = CharField(null=True)
    extra_time = BooleanField(null=True)
    full_time = BooleanField(null=True)
    half_time = BooleanField(null=True)
    home_team_goals = IntegerField(default=0)
    home_team_id = CharField()
    home_team_points = IntegerField(default=0)
    is_replay = BooleanField(constraints=[SQL("DEFAULT false")])
    match_date = DateField(null=True)
    match_time = TimeField(null=True)
    referee_id = CharField()
    venue_id = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'match'
        primary_key = CompositeKey('id_tag', 'version_num')

    def to_record(self):
        return self.to_model(MatchRecord)


class EditableMatch(DTO):
    away_team_goals: Optional[int]
    away_team_points: Optional[int]
    home_team_goals: Optional[int]
    home_team_points: Optional[int]
    away_team_manager_id: Optional[str]
    home_team_manager_id: Optional[str]
    extra_time: Optional[bool]
    full_time: Optional[bool]
    half_time: Optional[bool] 
    referee_id: Optional[str]
    match_time: Optional[str]
    match_date: Optional[date]


class Match(EditableMatch):
    away_team_id: str
    championship_id: str
    championship_round: str
    home_team_id: str
    is_replay: bool


class MatchRecord(Match):
    id_tag: str


class MatchResponseModel(ResponseModel):
    result: Optional[MatchRecord]


class MatchResponseModelList(ResponseModel):
    result: List[MatchRecord]
