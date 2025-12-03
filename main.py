import asyncio
import os
import httpx
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import create_db_and_tables
from router.user_router import user_router
from router.build_router import build_router
from router.component_router import component_router
from router.upload_router import upload_router
from config import configure_cloudinary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def keep_alive():
    """
    Pings the server every 14 minutes to prevent Render from sleeping.
    Relies on RENDER_EXTERNAL_URL environment variable.
    """
    url = os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        logger.info("RENDER_EXTERNAL_URL not set. Keep-alive task skipped.")
        return

    async with httpx.AsyncClient() as client:
        while True:
            try:
                logger.info(f"Sending keep-alive ping to {url}")
                response = await client.get(url)
                logger.info(f"Keep-alive ping status: {response.status_code}")
            except Exception as e:
                logger.error(f"Keep-alive ping failed: {e}")
            
            # Wait for 14 minutes (Render sleeps after 15 mins of inactivity)
            await asyncio.sleep(14 * 60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    configure_cloudinary()
    # Start the keep-alive task in the background
    asyncio.create_task(keep_alive())
    yield

app = FastAPI(lifespan=lifespan, title="PC Builder API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(user_router, prefix="/users")
app.include_router(build_router, prefix="/builds")
app.include_router(component_router, prefix="/components")
app.include_router(upload_router, prefix="/upload", tags=["Upload"])

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/img/logo.jpg")

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