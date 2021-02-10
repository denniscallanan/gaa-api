from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: str
    result: BaseModel
