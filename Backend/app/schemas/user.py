from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime
