from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
from router.user_router import user_router
from router.build_router import build_router
from router.component_router import component_router
from router.upload_router import upload_router
from config import configure_cloudinary

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    configure_cloudinary()
    yield

app = FastAPI(lifespan=lifespan, title="PC Builder API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(user_router, prefix="/users")
app.include_router(build_router, prefix="/builds")
app.include_router(component_router, prefix="/components")
app.include_router(upload_router, prefix="/upload", tags=["Upload"])

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