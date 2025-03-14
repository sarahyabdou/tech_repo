from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import LeadsInfo, UserInfo,UserRolePermission,UserRoleMapping,ClientCalls,ClientMeetings
from app.schemas import LeadCreate,UpdateLeadRequest
from app.schemas import CallCreate,MeetingCreate,CallResponse,MeetingResponse,AllLeadsResponse,LeadResponse
real_estate_router = APIRouter(dependencies=[Depends(get_current_user)])

@real_estate_router.post("/leads/")
def add_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):

    user = db.query(UserInfo).filter(UserInfo.id == lead_data.assigned_to).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    lead = LeadsInfo(**lead_data.dict())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"message": "Lead added successfully", "lead": lead}

# Assign a lead to a user
@real_estate_router.put("/leads/{lead_id}/assign/")
def assign_lead(lead_id: int, assigned_to: int, db: Session = Depends(get_db)):

    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    user = db.query(UserInfo).filter(UserInfo.id == assigned_to).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")


    lead.assigned_to = assigned_to
    db.commit()
    db.refresh(lead)
    return {"message": "Lead assigned successfully", "lead": lead}

def has_permission(db: Session, user_id: int, permission_type: str, module_id: int, feature_id: int) -> bool:

    user_roles = db.query(UserRoleMapping).filter(UserRoleMapping.user_id == user_id).all()
    for role_mapping in user_roles:
        # Check if the role has the required permission
        permission = db.query(UserRolePermission).filter(
            UserRolePermission.role_id == role_mapping.role_id,
            UserRolePermission.module_id == module_id,
            UserRolePermission.feature_id == feature_id
        ).first()
        if permission and getattr(permission, permission_type, False):
            return True
    return False
@real_estate_router.put("/leads/{lead_id}")
def edit_lead(
    lead_id: int,
    update_data: UpdateLeadRequest,
    user_id: int = Header(..., description="User ID from header"),
    db: Session = Depends(get_db)
):

    if not has_permission(db, user_id, "d_edit", module_id=1, feature_id=1):  # Replace with actual module and feature IDs
        raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to edit this lead")


    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)

    return {"message": "Lead updated successfully", "lead": lead}
@real_estate_router.delete("/leads/{lead_id}")
def delete_lead(
    lead_id: int,
    user_id: int = Header(..., description="User ID from header"),
    db: Session = Depends(get_db)
):

    if not has_permission(db, user_id, "d_delete", module_id=1, feature_id=1):  # Replace with actual module and feature IDs
        raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to delete this lead")


    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    db.delete(lead)
    db.commit()

    return {"message": "Lead deleted successfully"}
@real_estate_router.post("/leads/{lead_id}/calls")
def create_call(
    lead_id: int,
    call_data: CallCreate,
    user_id: int = Header(..., description="User ID from header"),
    db: Session = Depends(get_db)
):

    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    call = ClientCalls(
        assigned_to=call_data.assigned_to,
        company_domain=lead.company_domain,
        lead_id=lead_id,
        call_date=call_data.call_date,
        call_status=call_data.call_status
    )
    db.add(call)
    db.commit()
    db.refresh(call)

    return {"message": "Call created successfully", "call": call}

@real_estate_router.post("/leads/{lead_id}/meetings")
def create_meeting(
    lead_id: int,
    meeting_data: MeetingCreate,
    user_id: int = Header(..., description="User ID from header"),
    db: Session = Depends(get_db)
):

    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    meeting = ClientMeetings(
        assigned_to=meeting_data.assigned_to,
        company_domain=lead.company_domain,
        lead_id=lead_id,
        meeting_date=meeting_data.meeting_date,
        meeting_status=meeting_data.meeting_status
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return {"message": "Meeting created successfully", "meeting": meeting}

##
@real_estate_router.get("/leads/{lead_id}", response_model=LeadResponse)
def view_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):

    lead = db.query(LeadsInfo).filter(LeadsInfo.lead_id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")


    calls = db.query(ClientCalls).filter(ClientCalls.lead_id == lead_id).all()
    meetings = db.query(ClientMeetings).filter(ClientMeetings.lead_id == lead_id).all()


    lead_response = LeadResponse(
        lead_id=lead.lead_id,
        company_domain=lead.company_domain,
        lead_phone=lead.lead_phone,
        name=lead.name,
        assigned_to=lead.assigned_to,
        email=lead.email,
        gender=lead.gender,
        job_title=lead.job_title,
        lead_stage=lead.lead_stage,
        lead_type=lead.lead_type,
        lead_status=lead.lead_status,
        calls=[CallResponse(
            call_id=call.call_id,
            assigned_to=call.assigned_to,
            call_date=call.call_date,
            call_status=call.call_status
        ) for call in calls],
        meetings=[MeetingResponse(
            meeting_id=meeting.meeting_id,
            assigned_to=meeting.assigned_to,
            meeting_date=meeting.meeting_date,
            meeting_status=meeting.meeting_status
        ) for meeting in meetings]
    )

    return lead_response
@real_estate_router.get("/leads/", response_model=AllLeadsResponse)
def view_all_leads(
    db: Session = Depends(get_db)
):

    leads = db.query(LeadsInfo).all()


    leads_response = []
    for lead in leads:

        calls = db.query(ClientCalls).filter(ClientCalls.lead_id == lead.lead_id).all()
        meetings = db.query(ClientMeetings).filter(ClientMeetings.lead_id == lead.lead_id).all()


        leads_response.append(LeadResponse(
            lead_id=lead.lead_id,
            company_domain=lead.company_domain,
            lead_phone=lead.lead_phone,
            name=lead.name,
            assigned_to=lead.assigned_to,
            email=lead.email,
            gender=lead.gender,
            job_title=lead.job_title,
            lead_stage=lead.lead_stage,
            lead_type=lead.lead_type,
            lead_status=lead.lead_status,
            calls=[CallResponse(
                call_id=call.call_id,
                assigned_to=call.assigned_to,
                call_date=call.call_date,
                call_status=call.call_status
            ) for call in calls],
            meetings=[MeetingResponse(
                meeting_id=meeting.meeting_id,
                assigned_to=meeting.assigned_to,
                meeting_date=meeting.meeting_date,
                meeting_status=meeting.meeting_status
            ) for meeting in meetings]
        ))

    return AllLeadsResponse(leads=leads_response)