from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str = Field(default="", max_length=500)
    content: str = Field(default="", max_length=50000)
    is_favorite: bool = False


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, max_length=50000)
    is_favorite: Optional[bool] = None


class NoteResponse(NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    share_token: Optional[str] = None


class ShareResponse(BaseModel):
    share_url: str
    share_token: str


class SharedNoteResponse(BaseModel):
    title: str
    content: str
    created_at: datetime
