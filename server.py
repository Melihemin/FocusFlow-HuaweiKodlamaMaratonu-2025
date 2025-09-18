from fastapi import FastAPI, Request, Depends
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.main import router as main_router
from router.platform import router as platform_router
from database.models import Base, Person
from database.settings import engine, SessionLocal
from sqlalchemy.orm import Session

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Function to get DB session
def connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(connect)]

app.include_router(main_router)
app.include_router(platform_router)


# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# To run: uvicorn server:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)