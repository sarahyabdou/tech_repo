from app import app
from app.database import engine
from app.models import Base


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
