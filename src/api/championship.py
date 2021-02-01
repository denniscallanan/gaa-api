
from peewee import *
from playhouse.shortcuts import model_to_dict

from src.api.base import BaseModel
from src.api.exceptions import generic_error_wrapper


class Championship(BaseModel):
    championship_id = AutoField()
    championship_name = CharField()
    descript = CharField(null=True)

    class Meta:
        table_name = 'championship'


class ChampionshipClient:

    @generic_error_wrapper
    def get_championship(self, championship_id):
        championship = Championship.get_by_id(championship_id)
        return model_to_dict(championship)
