from fastapi import APIRouter, Depends, HTTPException

# from app.models import UserInfo
# from app.schemas import UserCreate, UserResponse
# from app.auth import get_password_hash
from sqlalchemy.orm import Session

# Create a router for user routes
router = APIRouter(prefix="/users", tags=["users"])

# Route to create a new user
# @router.post("/", response_model=UserResponse)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = get_password_hash(user.password)
#     db_user = User(
#         company_domain=user.company_domain,
#         first_name=user.first_name,
#         middle_name=user.middle_name,
#         last_name=user.last_name,
#         phone=user.phone,
#         email=user.email,
#         username=user.username,
#         password_hash=hashed_password,
#         gender=user.gender,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user