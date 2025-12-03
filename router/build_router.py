from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database import get_session
from models import Build, BuildCreate, User

build_router = APIRouter()   
templates = Jinja2Templates(directory="templates")

@build_router.get("/new", response_class=HTMLResponse)
def create_build_form(request: Request, session: Session = Depends(get_session)):
    users = session.query(User).all()
    return templates.TemplateResponse(
        "builds/new_build.html",
        {"request": request, "users": users}
    )

@build_router.post("/", response_class=HTMLResponse)
def create_build(
    request: Request,
    name: str = Form(...),
    user_id: int = Form(...),
    os: str = Form(...),
    bios_version: str = Form(...),
    session: Session = Depends(get_session)
):
    # 1. Crear la Build
    new_build = BuildCreate(name=name, user_id=user_id)
    build = Build.model_validate(new_build)
    session.add(build)
    session.commit()
    session.refresh(build)

    # 2. Crear la Configuración asociada
    from models import Configuration
    new_config = Configuration(build_id=build.id, os=os, bios_version=bios_version)
    session.add(new_config)
    session.commit()

    return RedirectResponse(url=f"/builds/{build.id}", status_code=302)



@build_router.get("/", response_class=HTMLResponse)
def list_users(request: Request, session: Session = Depends(get_session)):
    builds = session.query(Build).all()
    return templates.TemplateResponse("builds/build_list.html",
                                      {"request": request, "builds": builds})


@build_router.get("/{build_id}", response_class=HTMLResponse)
def get_build(request:Request, build_id: int, session:Session = Depends(get_session)):
    build = session.get(Build, build_id)
    if not build:
        raise HTTPException(404, "Build not found")
    
    return templates.TemplateResponse("builds/build_detail.html", {"request": request, "build": build})

@build_router.post("/{build_id}/delete")
def delete_build(build_id: int, session: Session = Depends(get_session)):
    build = session.get(Build, build_id)
    if not build:
        raise HTTPException(404, "Build not found")
    
    session.delete(build)
    session.commit()
    
    return RedirectResponse(url="/builds", status_code=302)
