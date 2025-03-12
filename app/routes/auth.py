# from fastapi import APIRouter, Depends, HTTPException
# from app.database import get_db
# # from app.models import UserInfo
# # from app.auth import get_current_user
# from sqlalchemy.orm import Session
#
# # Create a router for authentication routes
# router = APIRouter(prefix="/auth", tags=["auth"])
#
# # Example protected route
# @router.get("/protected")
# def read_protected(current_user: UserInfo = Depends(get_current_user)):
#     return {"message": "You are authenticated", "username": current_user.username}