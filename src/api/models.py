from pydantic import BaseModel


class RawParticipantData(BaseModel):
    rows: list
    headers: list
    file_name: str
