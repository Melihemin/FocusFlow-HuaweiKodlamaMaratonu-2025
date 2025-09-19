from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database.settings import SessionLocal
from typing import Annotated
from database.models import Lesson, User, User_statistics
from rag.model import generate_rag_answer

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

@router.get("/lessons/{lesson_id}/unit/{unit_id}", summary="Get Personalized Explanation of a Unit")
async def get_unit_lesson_detail(request: Request, unit_id: int, lesson_id: int, db: db_dependency):
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return JSONResponse(status_code=404, content={"message": "Lesson not found"})

    unit_content = getattr(lesson, f'unit_{unit_id}', None)
    if not unit_content:
        return JSONResponse(status_code=404, content={"message": "Unit not found"})
    
    unit_preview = " ".join(unit_content.split()[:20]) 

    rag_query = f"{lesson.title} dersi içindeki '{unit_preview}...' konusunu, DEHB'li bir bireyin kolayca anlayacağı şekilde yeniden anlat."

    response = generate_rag_answer(rag_query)

    return templates.TemplateResponse("unit_detail.html", {
        "request": request,
        "unit_id": unit_id,
        "lesson_id": lesson_id,
        "response": response # Pass the RAG-generated explanation
    })

@router.get("/user/{user_id}/statistics", summary="Get User Learning Statistics")
async def get_user_statistics(request: Request, user_id: int, db: db_dependency):


    return templates.TemplateResponse("dashboard.html", {"request": request, "user_id": user_id})