from peewee import *
from pydantic import BaseModel

from src.api.clients.base import BaseDataModel
from src.api.exceptions import generic_error_wrapper
from src.api.models.response_models import ResponseModel


class PortalUserTable(BaseDataModel):
    id_tag = AutoField()
    google_sub = CharField()
    reported_count = IntegerField(default=0)

    class Meta:
        table_name = 'portal_user'


class PortalUser(BaseModel):
    id_tag: int
    google_sub: str
    reported_count: int


class PortalUserResponseModel(ResponseModel):
    result: PortalUser


class PortalUserClient:

    @generic_error_wrapper
    def get_user_by_google_sub(self, google_sub_id):
        return PortalUserTable.get_or_none(PortalUserTable.google_sub == google_sub_id)

    @generic_error_wrapper
    def create_or_get_user_by_google_sub(self, google_sub_id):
        user = PortalUserTable.get_or_none(PortalUserTable.google_sub == google_sub_id)
        if not user:
            user = PortalUserTable(google_sub=google_sub_id)
            user.save()
        return user
