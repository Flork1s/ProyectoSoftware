from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_session
from models import Build, Component
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/builds", tags=["Builds"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
def list_builds(request: Request, db: Session = Depends(get_session)):
    builds = db.query(Build).all()
    return templates.TemplateResponse("builds.html", {"request": request, "builds": builds})

@router.get("/{build_id}")
def build_detail(build_id: int, request: Request, db: Session = Depends(get_session)):
    build = db.query(Build).filter(Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build no encontrada")
    return templates.TemplateResponse("build_detail.html", {"request": request, "build": build})

@router.post("/{build_id}/remove-component/{component_id}")
def remove_component(build_id: int, component_id: int, db: Session = Depends(get_session)):
    build = db.query(Build).filter(Build.id == build_id).first()
    component = db.query(Component).filter(Component.id == component_id).first()

    if not build or not component:
        raise HTTPException(status_code=404, detail="No encontrado")

    build.components.remove(component)
    db.commit()

    return RedirectResponse(f"/builds/{build_id}", status_code=302)

@router.post("/create")
def create_build(name: str = Form(...), db: Session = Depends(get_session)):
    build = Build(name=name)
    db.add(build)
    db.commit()
    return RedirectResponse("/builds", status_code=302)

@router.post("/{build_id}/delete")
def delete_build(build_id: int, db: Session = Depends(get_session)):
    build = db.query(Build).filter(Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build no encontrada")

    db.delete(build)
    db.commit()
    return RedirectResponse("/builds", status_code=302)
