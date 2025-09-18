from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from router.main import router as main_router

app = FastAPI()


app.include_router(main_router)


# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# To run: uvicorn server:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)