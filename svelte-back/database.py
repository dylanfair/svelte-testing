from typing import Optional, List, Union
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv
import os

from firebase_admin import firestore, initialize_app, credentials
from google.cloud.firestore import AsyncClient

# testing creds
load_dotenv()

default_app = initialize_app()
db = firestore.AsyncClient()
users_ref = db.collection('users')

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Todos(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    todo: str
    complete: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allwoed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "todo": "Play a game!",
                "complete": False
            }
        }

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password: str
    todos: Union[List[Todos], None] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "password": "12345",
                "todos": [
                    {
                        "todo": "Play a game!",
                        "complete": False
                    }
                ]
            }
        }

# class UpdateUserTodos(BaseModel):
#     todos: Optional[Union[List[Todos], None]]

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#              "example": {
#                 "name": "Jane Doe",
#                 "password": "12345",
#                 "todos": [
#                     {
#                         "todo": "Play a game!",
#                         "complete": False
#                     }
#                 ]
#             }
#         }





