from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, Field
from typing import List, Optional


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
class EmployeeCreate(BaseModel):
    company_domain: str
    contact_name: str
    business_phone: Optional[str] = None
    personal_phone: Optional[str] = None
    business_email: Optional[str] = None
    personal_email: Optional[str] = None
    gender: Optional[str] = None
    is_company_admin: bool = False
    user_uid: UUID

class SalaryCreate(BaseModel):
    company_domain: str
    employee_id: int
    gross_salary: float
    insurance: float
    taxes: float
    net_salary: float
    due_year: int
    due_month: int
    due_date: date

class EmployeeUpdate(BaseModel):
    contact_name: Optional[str] = None
    business_phone: Optional[str] = None
    personal_phone: Optional[str] = None
    business_email: Optional[str] = None
    personal_email: Optional[str] = None
    gender: Optional[str] = None
    is_company_admin: Optional[bool] = None

class SalaryUpdate(BaseModel):
    gross_salary: Optional[float] = None
    insurance: Optional[float] = None
    taxes: Optional[float] = None
    net_salary: Optional[float] = None
    due_year: Optional[int] = None
    due_month: Optional[int] = None
    due_date: Optional[date] = None

class SalaryResponse(BaseModel):
    gross_salary: float
    insurance: float
    taxes: float
    net_salary: float
    due_year: int
    due_month: int
    due_date: datetime

class EmployeeResponse(BaseModel):
    employee_id: int
    company_domain: str
    contact_name: str
    business_phone: Optional[str] = None
    personal_phone: Optional[str] = None
    business_email: Optional[str] = None
    personal_email: Optional[str] = None
    gender: Optional[str] = None
    is_company_admin: bool
    user_uid: str


class AllEmployeesResponse(BaseModel):
    employees: List[EmployeeResponse]