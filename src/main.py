from contextlib import asynccontextmanager

from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from chat.routes import router as chat_router
from filter.routes import router as api_router
from usage.routes import router as usage_router
from config_log import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gym-Project application is starting up via lifespan...")
    
    yield  
    
    logger.info("Gym-Project application is shutting down via lifespan...")

app = FastAPI(
  title = "Gym Backend",
  version = "1.0.0",
  lifespan=lifespan
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/{page_name}", response_class=HTMLResponse)
def serve_any_page(request: Request, page_name: str):
  if not page_name.endswith(".html"):
     page_name = f"{page_name}.html"

  template_path = BASE_DIR/"templates"/page_name

  if not template_path.is_file():
    raise HTTPException(status_code=404, detail="Page not found")
        
  return templates.TemplateResponse(request, name=page_name, context={})     

app.include_router(chat_router,prefix="/chat")
app.include_router(api_router,prefix="/api")
app.include_router(usage_router,prefix="/usage")
app.add_middleware(CORSMiddleware
  , allow_origins=["http://localhost:5173"]
  , allow_credentials=True
  , allow_methods=["*"]
  , allow_headers=["*"])

