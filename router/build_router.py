# router/build_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Build, Configuration
import crud

build_router = APIRouter(prefix="/builds", tags=["Builds"])

@build_router.post("/", response_model=Build)
def create_build(build: Build, session: Session = Depends(get_session)):
    return crud.create_build(session, build)

@build_router.get("/", response_model=list[Build])
def list_builds(session: Session = Depends(get_session)):
    return crud.get_builds(session)

@build_router.get("/{build_id}", response_model=Build)
def read_build(build_id: int, session: Session = Depends(get_session)):
    build = crud.get_build(session, build_id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build

@build_router.patch("/{build_id}", response_model=Build)
def update_build(build_id: int, build: Build, session: Session = Depends(get_session)):
    data = build.model_dump(exclude_unset=True)
    updated = crud.update_build(session, build_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Build not found")
    return updated

@build_router.delete("/{build_id}")
def delete_build(build_id: int, session: Session = Depends(get_session)):
    deleted = crud.delete_build(session, build_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Build not found")
    return {"message": "Build deleted"}

# Configuration (one-to-one)
@build_router.post("/{build_id}/configuration", response_model=Configuration)
def create_configuration_for_build(build_id: int, configuration: Configuration, session: Session = Depends(get_session)):
    # ensure build exists
    build = crud.get_build(session, build_id)
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    # attach
    configuration.build_id = build_id
    return crud.create_configuration(session, configuration)

@build_router.get("/{build_id}/configuration", response_model=Configuration)
def get_configuration_for_build(build_id: int, session: Session = Depends(get_session)):
    build = crud.get_build(session, build_id)
    if not build or not build.configuration:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return build.configuration
