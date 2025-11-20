# main.py
from fastapi import FastAPI
from database import create_db_and_tables
from router.user_router import user_router
from router.build_router import build_router
from router.component_router import component_router


app = FastAPI(title="PC Builder CRUD API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# include routers (each router already has prefix and tags)
app.include_router(user_router)
app.include_router(build_router)
app.include_router(component_router)

