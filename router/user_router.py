# router/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import User
import crud

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    return crud.create_user(session, user)

@user_router.get("/", response_model=list[User])
def list_users(session: Session = Depends(get_session)):
    return crud.get_users(session)

@user_router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session: Session = Depends(get_session)):
    data = user.model_dump(exclude_unset=True)
    updated = crud.update_user(session, user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@user_router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    deleted = crud.delete_user(session, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
