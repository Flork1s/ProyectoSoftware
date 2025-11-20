# router/component_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Component
import crud

component_router = APIRouter(prefix="/components", tags=["Components"])

@component_router.post("/", response_model=Component)
def create_component(comp: Component, session: Session = Depends(get_session)):
    return crud.create_component(session, comp)

@component_router.get("/", response_model=list[Component])
def list_components(session: Session = Depends(get_session)):
    return crud.get_components(session)

@component_router.get("/{component_id}", response_model=Component)
def read_component(component_id: int, session: Session = Depends(get_session)):
    comp = crud.get_component(session, component_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Component not found")
    return comp

@component_router.patch("/{component_id}", response_model=Component)
def update_component(component_id: int, comp: Component, session: Session = Depends(get_session)):
    data = comp.model_dump(exclude_unset=True)
    updated = crud.update_component(session, component_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Component not found")
    return updated

@component_router.delete("/{component_id}")
def delete_component(component_id: int, session: Session = Depends(get_session)):
    deleted = crud.delete_component(session, component_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Component not found")
    return {"message": "Component deleted"}
