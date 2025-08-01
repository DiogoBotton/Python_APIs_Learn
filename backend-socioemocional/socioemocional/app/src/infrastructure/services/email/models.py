from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class SenderSend(BaseModel):
    name: str
    email: str


class ToSend(BaseModel):
    email: str
    name: Optional[str] = None


class MessageVersion(BaseModel):
    to: List[ToSend]
    params: Optional[Dict[str, str]] = None
    subject: Optional[str] = None


class EmailTemplate(BaseModel):
    sender: SenderSend
    subject: str
    templateId: int
    params: Optional[Dict[str, str]] = None
    messageVersions: List[MessageVersion] = Field(default_factory=list)