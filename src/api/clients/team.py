from typing import Optional, List

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class TeamTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("TEAM"))
    est_year = SmallIntegerField(null=True)
    is_county = BooleanField(constraints=[SQL("DEFAULT true")])
    main_venue_id = CharField()
    sport = CharField(null=True)
    team_name = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'team'
        primary_key = CompositeKey('id_tag', 'version_num')

    def to_record(self):
        return self.to_model(TeamRecord)


class EditableTeam(DTO):
    main_venue_id: Optional[str]
    est_year: Optional[int]


class Team(EditableTeam):
    team_name: str
    sport: str
    is_county: bool


class TeamRecord(Team):
    id_tag: str
    

class TeamResponseModel(ResponseModel):
    result: Optional[TeamRecord]

class TeamResponseModelList(ResponseModel):
    result: List[TeamRecord]
