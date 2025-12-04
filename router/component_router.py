from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_session
from models import Component, Build
from fastapi.templating import Jinja2Templates

component_router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -----------------------------
# 1. FORMULARIO PARA CREAR COMPONENTE
# -----------------------------
@component_router.get("/new")
def new_component_form(request: Request):
    return templates.TemplateResponse(
        "components/new_component.html",
        {"request": request}
    )

# -----------------------------
# 2. CREAR COMPONENTE (POST)
# -----------------------------
@component_router.post("/new")
def create_component(
    request: Request,
    name: str = Form(...),
    kind: str = Form(...),
    brand: str = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_session)
):
    component = Component(
        name=name,
        kind=kind,
        brand=brand,
        price=price
    )
    db.add(component)
    db.commit()
    db.refresh(component)

    return RedirectResponse(f"/components/{component.id}", status_code=302)

# -----------------------------
# 3. LISTAR COMPONENTES
# -----------------------------
@component_router.get("/")
def list_components(request: Request, db: Session = Depends(get_session)):
    # components = db.query(Component).all()  <-- Ya no se muestra la lista completa
    return templates.TemplateResponse(
        "components/component_list.html",
        {"request": request} #, "components": components}
    )

# -----------------------------
# 3.1 LISTAR POR TIPO
# -----------------------------
@component_router.get("/type/{kind}")
def list_components_by_kind(kind: str, request: Request, db: Session = Depends(get_session)):
    # Filtrar componentes por el campo 'kind'
    # Es importante que 'kind' coincida con los valores en la BD (CPU, GPU, etc.)
    components = db.query(Component).filter(Component.kind == kind).all()
    
    return templates.TemplateResponse(
        "components/components_by_kind.html",
        {
            "request": request, 
            "components": components, 
            "kind_title": kind  # Para mostrar el título en el template
        }
    )



# -----------------------------
# 4. VER DETALLE
# -----------------------------
@component_router.get("/{component_id}")
def component_detail(component_id: int, request: Request, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()
    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    return templates.TemplateResponse(
        "components/component_detail.html",
        {"request": request, "component": component}
    )

# -----------------------------
# 5. FORMULARIO ASIGNAR
# -----------------------------
@component_router.get("/{component_id}/assign")
def assign_form(component_id: int, request: Request, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()
    builds = db.query(Build).all()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")

    return templates.TemplateResponse(
        "components/assign_component.html",
        {"request": request, "component": component, "builds": builds}
    )

# -----------------------------
# 6. POST ASIGNAR
# -----------------------------
@component_router.post("/{component_id}/assign")
def assign_component_to_build(
    component_id: int,
    build_id: int = Form(...),
    db: Session = Depends(get_session)
):
    component = db.query(Component).filter(Component.id == component_id).first()
    build = db.query(Build).filter(Build.id == build_id).first()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    
    if not build:
        raise HTTPException(status_code=404, detail=f"No existe una build con id = {build_id}")

    # Asignar componente a la build
    build.components.append(component)
    db.commit()

    return RedirectResponse(f"/components/{component.id}", status_code=302)

# -----------------------------
# 7. ELIMINAR
# -----------------------------
@component_router.post("/{component_id}/delete")
def delete_component(component_id: int, db: Session = Depends(get_session)):
    component = db.query(Component).filter(Component.id == component_id).first()

    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")

    db.delete(component)
    db.commit()
    return RedirectResponse("/components", status_code=302)
