
from peewee import *
from playhouse.db_url import connect

from src.constants import ServerConfig

db = connect(ServerConfig.DATABASE_URL, autorollback=True)

class BaseModel(Model):
    class Meta:
        database = db
