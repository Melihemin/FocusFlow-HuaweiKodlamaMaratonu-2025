from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database.settings import SessionLocal
from typing import Annotated
from database.models import Lesson, User, User_statistics

router = APIRouter(prefix="/education", tags=["Education Platform"])

# Mount static files directory
router.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Function to get DB session
def connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(connect)]

@router.get("/lessons", summary="Education Platform Home Page")
async def get_lessons(request: Request, db: db_dependency):
    lessons = db.query(Lesson).all()
    print([lesson.title for lesson in lessons] if lessons else "No lessons found")
    return templates.TemplateResponse("lessons.html", {"request": request, "lessons": lessons})

@router.get("/lessons/{lesson_id}", summary="Education Platform Lesson Detail Page")
async def get_lesson_detail(request: Request, lesson_id: int, db: db_dependency):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return JSONResponse(status_code=404, content={"message": "Lesson not found"})
    return templates.TemplateResponse("lesson_detail.html", {"request": request, "lesson": lesson})

@router.get("/lessons/{lesson_id}/unit/{unit_id}", summary="Education Platform Unit Lesson Detail Page")
async def get_unit_lesson_detail(request: Request, unit_id: int, lesson_id: int):
    return templates.TemplateResponse("unit_detail.html", {"request": request, "unit_id": unit_id, "lesson_id": lesson_id})