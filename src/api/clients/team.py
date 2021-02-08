from typing import Optional

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


class Team(DTO):
    team_name: Optional[str]
    main_venue_id: Optional[str]
    sport: Optional[str]
    is_county: Optional[bool]
    est_year: Optional[int]

    @classmethod
    def get_required_fields(cls):
        return ["team_name", 'is_county']

    @classmethod
    def get_uneditable_fields(cls):
        return ["team_name", "sport"]


class TeamResponseModel(ResponseModel):
    result: Optional[Team.get_identified_record()]
