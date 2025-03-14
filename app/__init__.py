

from fastapi import FastAPI , Depends
from app.auth import get_current_user
from app.hr.routes import hr_router
from app.models import UserInfo

# Create the FastAPI app
app = FastAPI()

