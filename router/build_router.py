from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database import get_session
from models import Build, BuildCreate, Component

router = APIRouter()   
templates = Jinja2Templates(directory="templates")

@router.get("/new", response_class=HTMLResponse)
def create_build_form(request:Request):
    return templates.TemplateResponse("builds/new_build.html", {"request":request})


@router.post("/", response_class=HTMLResponse)
def create_build(
    request:Request,
    id: int = Form(...),
    name: str = Form(...),
    #user_id: int = Form(...),
    session:Session = Depends(get_session)
):
    new_build = BuildCreate(id=id, name=name)
    build = Build.model_validate(new_build)
    session.add(build)
    session.commit()
    session.refresh(build)

    return RedirectResponse(url= f"/builds/{build.id}", status_code=302)


@router.get("/", response_class=HTMLResponse)
def list_users(request: Request, session: Session = Depends(get_session)):
    builds = session.query(Build).all()
    return templates.TemplateResponse("builds/build_list.html",
                                      {"request": request, "builds": builds})


@router.get("/{build_id}", response_class=HTMLResponse)
def get_build(request:Request, build_id: int, session:Session = Depends(get_session)):
    build = session.get(Build, build_id)
    if not build:
        raise HTTPException(404, "Build not found")
    
    return templates.TemplateResponse("builds/build_detail.html", {"request": request, "build": build})

