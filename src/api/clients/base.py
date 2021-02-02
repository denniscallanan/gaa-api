
from peewee import *
from playhouse.db_url import connect

from src.api.models.response_models import ResponseModel
from src.constants import ServerConfig

db = connect(ServerConfig.DATABASE_URL, autorollback=True)


class BaseDataModel(Model):
    class Meta:
        database = db


class BaseClient:

    def to_response_model(self, item: ResponseModel, success=True):
        status = "success" if success else "failure"
        return ResponseModel(status=status, result=item)

    def _get_field_args(self, db_model, new_field_map=None, discarded_fields=None):

        attributes = db_model.__dict__['__data__']
        field_map = new_field_map or {}
        fields_to_discard = discarded_fields or set([])

        field_args = {}
        for k in list(attributes.keys()):
            if k not in fields_to_discard:
                if k in field_map and field_map[k] is not None:
                    field_args[field_map[k]] = attributes[k]
                else:
                    field_args[k] = attributes[k]
        return field_args
