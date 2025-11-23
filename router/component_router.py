# router/user_router.py
from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database import get_session
from models import Component, ComponentCreate

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/new", response_class=HTMLResponse)
def create_component_form(request: Request):
    return templates.TemplateResponse("components/new_component.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
def create_component(
    request: Request,
    id: int = Form(...),
    name: str = Form(...),
    kind: str = Form(...),
    brand: str = Form(...),
    price: float = Form(...),
    session: Session = Depends(get_session)
):
    new_component = ComponentCreate(id=id, name=name, kind=kind, brand=brand,price=price)
    component = Component.model_validate(new_component)
    session.add(component)
    session.commit()
    session.refresh(component)

    return RedirectResponse(url=f"/components/{component.id}", status_code=302)

@router.get("/", response_class=HTMLResponse)
def list_component(request: Request, session: Session = Depends(get_session)):
    components = session.query(Component).all()
    return templates.TemplateResponse("components/component_list.html",
                                      {"request": request, "omponents": components})

@router.get("/{component_id}", response_class=HTMLResponse)
def get_component(request: Request, component_id: int, session: Session = Depends(get_session)):
    component = session.get(Component, component_id)
    if not component:
        raise HTTPException(404, "Component not found")

    return templates.TemplateResponse("components/component_detail.html",
                                      {"request": request, "component": component})
