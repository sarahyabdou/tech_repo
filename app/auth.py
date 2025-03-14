from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.models import UserInfo
from app.database import get_db



security = HTTPBasic()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserInfo).filter(UserInfo.username == username).first()
    if not user:
        return False
    if password != user.password_hash:
        return False
    return user

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    print("get_current_user called")  # Debugging
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user