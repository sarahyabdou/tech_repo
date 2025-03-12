from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Date, TIMESTAMP, UUID, ForeignKey, Numeric, ForeignKeyConstraint,
    BigInteger, func, text,
)
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint, ForeignKeyConstraint

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    display_name = Column(String(100))
    description = Column(Text)
    available = Column(Boolean)
    comming_on = Column(Date)
    color = Column(BigInteger)
    url = Column(Text)


class ModuleFeature(Base):
    __tablename__ = 'module_features'
    module_id = Column(Integer, ForeignKey('modules.id'), primary_key=True)
    feature_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    display_name = Column(String(100))

# Company Info Table
class CompanyInfo(Base):
    __tablename__ = 'company_info'
    company_domain = Column(String(100), primary_key=True)
    name = Column(String(50), nullable=False)
    field = Column(String(100))
    address = Column(String(500))
    country = Column(String(100))
    telephone_number = Column(String(50), unique=True, nullable=False)
    date_added = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')


class UserInfo(Base):
    __tablename__ = 'user_info'
    date_added = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
    id = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    company_domain = Column(String(100), ForeignKey('company_info.company_domain'))
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    phone = Column(String(50), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200))
    gender = Column(String(10))
    leads = relationship("LeadsInfo", back_populates="assigned_user")



class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_domain = Column(String(100), ForeignKey('company_info.company_domain'))
    module_id = Column(Integer, ForeignKey('modules.id'))
    name = Column(String(50), nullable=False)


    __table_args__ = (
        UniqueConstraint('company_domain', 'module_id', 'name', name='uq_user_roles'),
    )

    # Relationships
    permissions = relationship("UserRolePermission", back_populates="role")
    user_mappings = relationship("UserRoleMapping", back_populates="role")


class UserRolePermission(Base):
    __tablename__ = 'user_role_permissions'

    role_id = Column(Integer, ForeignKey('user_roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, nullable=False)
    feature_id = Column(Integer, nullable=False)
    d_read = Column(Boolean, default=False)
    d_write = Column(Boolean, default=False)
    d_edit = Column(Boolean, default=False)
    d_delete = Column(Boolean, default=False)

    # Foreign key to module_features (composite foreign key)
    __table_args__ = (
        ForeignKeyConstraint(
            ['module_id', 'feature_id'],
            ['module_features.module_id', 'module_features.feature_id']
        ),
    )


    role = relationship("UserRole", back_populates="permissions")


class UserRoleMapping(Base):
    __tablename__ = 'user_role_mapping'

    user_id = Column(Integer, ForeignKey('user_info.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(Integer, ForeignKey('user_roles.id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    user = relationship("UserInfo", back_populates="role_mappings")
    role = relationship("UserRole", back_populates="user_mappings")
#
class LeadsStage(Base):
    __tablename__ = 'leads_stage'

    company_domain = Column(String(100), ForeignKey('company_info.company_domain'), primary_key=True)
    id = Column(Integer, primary_key=True)
    lead_stage = Column(String(50))
    date_added = Column(TIMESTAMP, server_default=func.now())

    is_assigned = Column(Boolean)
    is_not_assigned = Column(Boolean)
    is_action_taken = Column(Boolean)

    leads = relationship("LeadsInfo", back_populates="stage")
class LeadsStatus(Base):
    __tablename__ = 'leads_status'

    company_domain = Column(String(100), ForeignKey('company_info.company_domain'), primary_key=True)
    id = Column(Integer, primary_key=True)
    lead_status = Column(String(50))
    date_added = Column(TIMESTAMP, server_default=func.now())
    leads = relationship("LeadsInfo", back_populates="status")
class LeadsType(Base):
    __tablename__ = 'leads_types'

    company_domain = Column(String(100), ForeignKey('company_info.company_domain'), primary_key=True)
    id = Column(Integer, primary_key=True)
    lead_type = Column(String(50))
    date_added = Column(TIMESTAMP, server_default=func.now())
    leads = relationship("LeadsInfo", back_populates="type")
class MeetingsStatus(Base):
    __tablename__ = 'meetings_status'

    company_domain = Column(String(100), ForeignKey('company_info.company_domain'), primary_key=True)
    id = Column(Integer, primary_key=True)
    meeting_status = Column(String(50))
    date_added = Column(TIMESTAMP, server_default=func.now())
class CallsStatus(Base):
    __tablename__ = 'calls_status'

    company_domain = Column(String(100), ForeignKey('company_info.company_domain'), primary_key=True)
    id = Column(Integer, primary_key=True)
    call_status = Column(String(50))
    date_added = Column(TIMESTAMP, server_default=func.now())

class LeadsInfo(Base):
    __tablename__ = 'leads_info'

    date_added = Column(TIMESTAMP, server_default=func.now())
    lead_id = Column(Integer, primary_key=True, autoincrement=True)
    company_domain = Column(String(100), nullable=False)
    lead_phone = Column(String(50), unique=True, nullable=False)
    name = Column(String(50))
    assigned_to = Column(Integer, ForeignKey('user_info.id'))
    email = Column(String(50))
    gender = Column(String(10))
    job_title = Column(String(100))
    lead_stage = Column(Integer)
    lead_type = Column(Integer)
    lead_status = Column(Integer)


    __table_args__ = (
        ForeignKeyConstraint(
            ['company_domain', 'lead_stage'],
            ['leads_stage.company_domain', 'leads_stage.id']
        ),
        ForeignKeyConstraint(
            ['company_domain', 'lead_type'],
            ['leads_types.company_domain', 'leads_types.id']
        ),
        ForeignKeyConstraint(
            ['company_domain', 'lead_status'],
            ['leads_status.company_domain', 'leads_status.id']
        ),
    )


    assigned_user = relationship("UserInfo", back_populates="leads")
    stage = relationship("LeadsStage", back_populates="leads")
    type = relationship("LeadsType", back_populates="leads")
    status = relationship("LeadsStatus", back_populates="leads")
class ClientMeetings(Base):
    __tablename__ = 'client_meetings'

    meeting_id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(TIMESTAMP, server_default=func.now())
    assigned_to = Column(Integer, ForeignKey('user_info.id'))
    company_domain = Column(String(100), ForeignKey('company_info.company_domain'))
    lead_id = Column(Integer, ForeignKey('leads_info.lead_id'))
    meeting_date = Column(TIMESTAMP)
    meeting_status = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ['company_domain', 'meeting_status'],
            ['meetings_status.company_domain', 'meetings_status.id']
        ),
    )
class ClientCalls(Base):
    __tablename__ = 'client_calls'

    call_id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(TIMESTAMP, server_default=func.now())
    assigned_to = Column(Integer, ForeignKey('user_info.id'))
    company_domain = Column(String(100), ForeignKey('company_info.company_domain'))
    lead_id = Column(Integer, ForeignKey('leads_info.lead_id'))
    call_date = Column(TIMESTAMP)
    call_status = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ['company_domain', 'call_status'],
            ['calls_status.company_domain', 'calls_status.id']
        ),
    )