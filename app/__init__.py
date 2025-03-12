
# Include the routes
# app.include_router(auth.router)
# app.include_router(users.router)
# # Include API routers
# app.include_router(hr_router, prefix="/hr", tags=["HR"])
# app.include_router(real_estate_router, prefix="/real-estate", tags=["Real Estate"])
from fastapi import FastAPI , Depends
from app.auth import get_current_user
from app.models import UserInfo

# Create the FastAPI app
app = FastAPI()

# Protected route
@app.get("/protected/")
def protected_route(current_user: UserInfo = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! You are authenticated."}

# Public route
@app.get("/public/")
def public_route():
    return {"message": "This is a public route."}