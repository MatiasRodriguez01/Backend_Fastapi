from pydantic import BaseModel
from bson.objectid import ObjectId

class UserDB(BaseModel):
    _id: ObjectId
    username: str
    password: str
    email: str
    role: str
    age: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: lambda x: str(x)
        }