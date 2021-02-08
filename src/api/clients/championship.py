from typing import Optional

from peewee import *

from src.api.clients.base import DTO, BaseDataModel
from src.api.models.response_models import ResponseModel


class ChampionshipTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("VEN"))
    championship_name = CharField()
    descript = CharField(null=True)
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'championship'
        primary_key = CompositeKey('id_tag', 'version_num')


class Championship(DTO):
    championship_name: Optional[str]
    descript: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["championship_name"]

    @classmethod
    def get_uneditable_fields(cls):
        return ["championship_name"]

class ChampionshipResponseModel(ResponseModel):
    result: Championship.get_identified_record()
