
from fastapi import APIRouter, Depends, Request


router = APIRouter(prefix="/", tags=["Home"])


@router.get("/", summary="Home Page")
async def read_root(request: Request):
    return {"message": "Welcome to the Home Page"}