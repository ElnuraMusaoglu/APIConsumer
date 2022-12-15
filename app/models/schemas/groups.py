from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, BaseConfig


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True


class RWSchema(RWModel):
    class Config(RWModel.Config):
        orm_mode = True


class GroupClusterSchema(RWModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)
    transaction_id: str = Field(..., min_length=20, max_length=100)


class GroupClusterDB(GroupClusterSchema):
    id: int
    #transaction_timestamp: str = Field(..., min_length=5, max_length=50)


class GroupSchema(RWModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)


class GroupSchemaTransaction(GroupSchema):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=100)
    transaction_id: str = Field(..., min_length=20, max_length=100)
    #transaction_timestamp: str = Field(..., min_length=5, max_length=50)


class GroupDB(GroupSchemaTransaction):
    id: int


class GroupDeleteSchema(RWModel):
    transaction_id: str = None


class GroupDeleteDB(GroupDeleteSchema):
    id: int


class ListOfGroupDeleteDB(RWModel):
    groups: List[GroupDeleteDB]
