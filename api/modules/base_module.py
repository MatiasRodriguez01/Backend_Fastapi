from typing import Optional
from pydantic import BaseModel

class Base(BaseModel):
    id: Optional[str] = None