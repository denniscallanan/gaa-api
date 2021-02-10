from typing import Optional, List

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

    def to_record(self):
        return self.to_model(ChampionshipRecord)


class EditableChampionship(DTO):
    descript: Optional[str]


class Championship(EditableChampionship):
    championship_name: str


class ChampionshipRecord(Championship):
    id_tag: str


class ChampionshipResponseModel(ResponseModel):
    result: Optional[ChampionshipRecord]


class ChampionshipResponseModelList(ResponseModel):
    result: List[ChampionshipRecord]
