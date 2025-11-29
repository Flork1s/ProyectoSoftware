# router/user_router.py
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database import get_session
from models import User, UserCreate

user_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@user_router.get("/new", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse("users/new_user.html", {"request": request})

@user_router.post("/", response_class=HTMLResponse)
def create_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    session: Session = Depends(get_session)
):
    new_user = UserCreate(name=name, email=email)
    user = User.model_validate(new_user)
    session.add(user)
    session.commit()
    session.refresh(user)

    return RedirectResponse(url=f"/users/{user.id}", status_code=302)

@user_router.get("/", response_class=HTMLResponse)
def list_users(request: Request, session: Session = Depends(get_session)):
    users = session.query(User).all()
    return templates.TemplateResponse("users/user_list.html",
                                      {"request": request, "users": users})

@user_router.get("/{user_id}", response_class=HTMLResponse)
def get_user(request: Request, user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    return templates.TemplateResponse("users/user_detail.html",
                                      {"request": request, "user": user})