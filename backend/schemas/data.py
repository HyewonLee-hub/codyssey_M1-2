from pydantic import BaseModel


class DataCreate(BaseModel):
    date: str
    value: float
    memo: str = ""


class DataUpdate(BaseModel):
    value: float
    memo: str = ""