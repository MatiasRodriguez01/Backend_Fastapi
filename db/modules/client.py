from typing import Optional
from pydantic import BaseModel

class Client(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    url: str