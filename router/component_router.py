# router/component_router.py
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database import get_session
from models import Component, ComponentCreate, Build
from Kind import Kind


component_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@component_router.get("/", response_class=HTMLResponse)
def list_components(request: Request, session: Session = Depends(get_session)):
    components = session.query(Component).all()
    return templates.TemplateResponse(
        "components/component_list.html",
        {"request": request, "components": components}
    )


@component_router.get("/new", response_class=HTMLResponse)
def new_component_form(request: Request, session: Session = Depends(get_session)):
    builds = session.query(Build).all()
    return templates.TemplateResponse(
        "components/new_component.html",
        {"request": request, "builds": builds, "kinds": list(Kind)}
    )


@component_router.post("/")
def create_component(
    name: str = Form(...),
    brand: str = Form(...),
    price: float = Form(...),
    kind: Kind = Form(...),
    build_id: int = Form(None),
    session: Session = Depends(get_session)
):
    new_component = ComponentCreate(
        name=name,
        brand=brand,
        price=price,
        kind=kind,
        build_id=build_id
    )
    comp = Component.model_validate(new_component)
    session.add(comp)
    session.commit()
    session.refresh(comp)
    return RedirectResponse(url=f"/components/{comp.id}", status_code=302)


@component_router.get("/{component_id}", response_class=HTMLResponse)
def get_component(request: Request, component_id: int, session: Session = Depends(get_session)):
    comp = session.get(Component, component_id)
    if not comp:
        raise HTTPException(404, "Componente no encontrado")
    return templates.TemplateResponse(
        "components/component_detail.html",
        {"request": request, "component": comp}
    )
