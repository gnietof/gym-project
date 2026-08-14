from dotenv import load_dotenv

load_dotenv()


import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config_log import setup_logging
from routes.chat_routes import router as chat_router
from routes.filter_routes import router as api_router
from routes.prompt_routes import router as prompt_router
from routes.usage_routes import router as usage_router

setup_logging()


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gym-Project application is starting up via lifespan...")

    yield

    logger.info("Gym-Project application is shutting down via lifespan...")


app = FastAPI(title="Gym Backend", version="1.0.0", lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/{page_name}", response_class=HTMLResponse)
def serve_any_page(request: Request, page_name: str):
    if not page_name.endswith(".html"):
        page_name = f"{page_name}.html"

    template_path = BASE_DIR / "templates" / page_name

    if not template_path.is_file():
        raise HTTPException(status_code=404, detail="Page not found")

    return templates.TemplateResponse(request, name=page_name, context={})


app.include_router(chat_router, prefix="/chat")
app.include_router(api_router, prefix="/api")
app.include_router(usage_router, prefix="/usage")
app.include_router(prompt_router, prefix="/prompt")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
