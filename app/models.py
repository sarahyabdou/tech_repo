from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Date, TIMESTAMP, UUID, ForeignKey, Numeric, ForeignKeyConstraint,BigInteger,
)
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

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

#  User Info Table
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

