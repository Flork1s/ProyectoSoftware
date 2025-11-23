from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_session
from models import Component, Build
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/components", tags=["Components"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def list_components(request: Request, db: Session = Depends(get_session)):
    components = db.query(Component).all()
    return templates.TemplateResponse("components.html", {"request": request, "components": components})


@router.get("/{component_id}")
def component_detail(component_id: int, request: Request, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return templates.TemplateResponse("component_detail.html", {"request": request, "component": component})


@router.get("/{component_id}/assign")
def assign_form(component_id: int, request: Request, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()
    builds = db.query(Build).all()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")

    return templates.TemplateResponse(
        "assign_component.html",
        {"request": request, "component": component, "builds": builds}
    )


@router.post("/{component_id}/assign")
def assign_component_to_build(
    component_id: int,
    build_id: int,
    db: Session = Depends(get_session)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    build = db.query(Build).filter(Build.id == build_id).first()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    
    if not build:
        raise HTTPException(status_code=404, detail=f"No existe una build con id = {build_id}")

    # Aquí sí lo asignamos
    build.components.append(component)
    db.commit()

    return RedirectResponse(f"/components/{component.id}", status_code=302)



@router.post("/{component_id}/delete")
def delete_component(component_id: int, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")

    db.delete(component)
    db.commit()
    return RedirectResponse("/components", status_code=302)
