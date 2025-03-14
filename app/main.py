from app import app
from app.database import engine
from app.hr.routes import hr_router
from app.models import Base

from app.real_estate.routes import real_estate_router
from app.hr.routes import hr_router

Base.metadata.create_all(bind=engine)
app.include_router(real_estate_router, prefix="/real_estate", tags=["Real Estate"])
app.include_router(hr_router, prefix="/hr", tags=["HR"])



if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
