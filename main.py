from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database import create_db_and_tables
from router.user_router import user_router
from router.build_router import build_router
from router.component_router import component_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="PC Builder API")

# 📌 Carpeta de templates (SOLO HTML, como dijo el profesor)
templates = Jinja2Templates(directory="templates")

# 📌 Routers (API + HTML)
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(build_router, prefix="/builds", tags=["builds"])
app.include_router(component_router, prefix="/components", tags=["components"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.exception_handler(HTTPException)
async def error_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html",
                                      {"request": request,
                                       "status_code": exc.status_code,
                                       "detail": exc.detail},
                                      status_code=exc.status_code)
