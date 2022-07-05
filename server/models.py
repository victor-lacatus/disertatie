import typing
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Any, Optional
from pymongo import MongoClient

client = MongoClient()
db = client.test

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    username: str
    email: str
    role: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        
class DataSet(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    created_by: str
    data: Optional[Any]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }