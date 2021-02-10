from typing import Optional, List

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

    def to_record(self):
        return self.to_model(VenueRecord)


class EditableVenue(DTO):
    year_built: Optional[int]


class Venue(EditableVenue):
    venue_county: str
    venue_name: str


class VenueRecord(Venue):
    id_tag: str


class VenueResponseModel(ResponseModel):
    result: Optional[VenueRecord]


class VenueResponseModelList(ResponseModel):
    result: List[VenueRecord]
