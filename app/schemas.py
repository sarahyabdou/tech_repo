from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class LeadCreate(BaseModel):
    company_domain: str
    lead_phone: str
    name: str
    assigned_to: int
    email: str
    gender: str
    job_title: str
    lead_stage: int
    lead_type: int
    lead_status: int
class UpdateLeadRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    lead_phone: Optional[str] = None
    gender: Optional[str] = None
    job_title: Optional[str] = None
    lead_stage: Optional[int] = None
    lead_type: Optional[int] = None
    lead_status: Optional[int] = None
class CallCreate(BaseModel):
    assigned_to: int
    call_date: datetime
    call_status: int

class MeetingCreate(BaseModel):
    assigned_to: int
    meeting_date: datetime
    meeting_status: int
class CallResponse(BaseModel):
    call_id: int
    assigned_to: int
    call_date: datetime
    call_status: int

class MeetingResponse(BaseModel):
    meeting_id: int
    assigned_to: int
    meeting_date: datetime
    meeting_status: int
class LeadResponse(BaseModel):
    lead_id: int
    company_domain: str
    lead_phone: str
    name: str
    assigned_to: int
    email: str
    gender: str
    job_title: str
    lead_stage: int
    lead_type: int
    lead_status: int
    calls: list[CallResponse]
    meetings: list[MeetingResponse]

class AllLeadsResponse(BaseModel):
    leads: list[LeadResponse]