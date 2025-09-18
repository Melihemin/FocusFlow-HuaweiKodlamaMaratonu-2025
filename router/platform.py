from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/education", tags=["Education Platform"])

# Mount static files directory
router.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")


@router.get("/lessons", summary="Education Platform Home Page")
async def get_lessons(request: Request):
    return templates.TemplateResponse("lessons.html", {"request": request})