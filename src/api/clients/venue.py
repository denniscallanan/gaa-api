from typing import Optional

from peewee import *

from src.api.clients.base import BaseDataModel, DTO
from src.api.models.response_models import ResponseModel


class VenueTable(BaseDataModel):
    id_tag = CharField(default=BaseDataModel.gen_uid("VEN"))
    year_built = IntegerField(null=True)
    venue_county = CharField(null=True)
    venue_name = CharField()
    version_num = IntegerField(null=False, default=0)
    created_by = IntegerField(null=False, default=0)
    recorded_timestamp = DateTimeField(null=False, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'venue'
        primary_key = CompositeKey('id_tag', 'version_num')


class Venue(DTO):
    year_built: Optional[int]
    venue_county: Optional[str]
    venue_name: Optional[str]

    @classmethod
    def get_required_fields(cls):
        return ["venue_name", 'venue_county']

    @classmethod
    def get_uneditable_fields(cls):
        return ["venue_name", "venue_county"]


class VenueResponseModel(ResponseModel):
    result: Venue.get_identified_record()
