class WebFastApiFactory:
    """
    Concrete Factory tạo router backend FastAPI.
    """

    @staticmethod
    def get_fastapi_router_template(
        pascal_name: str, snake_name: str, group: str = ""
    ) -> str:
        kebab = snake_name.replace("_", "-")
        usecase_subpath = f"{group}.{snake_name}" if group else snake_name
        return f"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.{usecase_subpath}.{snake_name}_dto import {pascal_name}Input
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/{kebab}", tags=["{pascal_name}"])

class {pascal_name}Request(BaseModel):
    data: Optional[Dict[str, Any]] = None

def get_context():
    return AppContextWeb()

@router.post("/")
async def {snake_name}_endpoint(request: {pascal_name}Request, context: AppContextWeb = Depends(get_context)):
    logger.info("Received request at {pascal_name} endpoint")
    try:
        current_controller = "Web{pascal_name}Controller"
        controller = context.container.resolve(current_controller)
        if not controller:
            raise HTTPException(status_code=500, detail=f"Controller {{current_controller}} not resolved")
        payload = request.data if request.data else {{}}
        response = await controller.execute(payload)
        if response.get("status") == "success":
            return {{"status": "success", "message": response.get("message", "Success")}}
        raise HTTPException(status_code=400, detail=f"Failed: {{response.get('message')}}")
    except ValueError as e:
        logger.error(f"Validation error: {{str(e)}}")
        raise HTTPException(status_code=400, detail=str(e))
"""

    @staticmethod
    def get_fastapi_debug_router_template() -> str:
        return """from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
import os
import re

router = APIRouter(prefix="/api/v1/debug", tags=["Debug"])

class ScreenshotRequest(BaseModel):
    image: str
    filename: str
    overwrite: bool = False

@router.post("/save-screenshot")
async def save_screenshot(request: ScreenshotRequest):
    try:
        image_data = request.image
        if "," in image_data:
            image_data = image_data.split(",")[1]
            
        decoded = base64.b64decode(image_data)
        clean_filename = re.sub(r"[^a-zA-Z0-9_.-]", "_", request.filename)
        
        if request.overwrite:
            os.makedirs("artifacts", exist_ok=True)
            file_path = os.path.join("artifacts", clean_filename)
        else:
            os.makedirs("artifacts/snapshots", exist_ok=True)
            name_part, ext_part = os.path.splitext(clean_filename)
            idx = 1
            while True:
                filename = f"{name_part}_{idx}{ext_part}"
                file_path = os.path.join("artifacts/snapshots", filename)
                if not os.path.exists(file_path):
                    break
                idx += 1
                
        with open(file_path, "wb") as f:
            f.write(decoded)
            
        rel_path = os.path.relpath(file_path)
        return {"status": "success", "message": f"Saved screenshot to {rel_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pages")
async def list_pages():
    try:
        frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
        pages_dir = os.path.join(frontend_dir, "level_05_pages")
        if not os.path.exists(pages_dir):
            return {"pages": []}
        pages = []
        for file in os.listdir(pages_dir):
            if file.endswith(".html") and file != "welcome.html":
                route_name = os.path.splitext(file)[0].replace("_", "-")
                display_name = os.path.splitext(file)[0].replace("_", " ").title()
                pages.append({"route": f"/{route_name}", "name": display_name})
        return {"pages": pages}
    except Exception as e:
        return {"pages": []}
"""

    @staticmethod
    def get_fastapi_main_template(project_name: str) -> str:
        return f"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")))

from src.layer_05_bootstrap.app_context_web import AppContextWeb
from src.layer_04_infrastructure.ui.web_fastapi.fastapi.routers import debug

def create_app() -> FastAPI:
    app = FastAPI(title="{project_name} Web API", version="1.0.0")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    context = AppContextWeb()
    
    app.include_router(debug.router)
    
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
    
    from fastapi.responses import HTMLResponse
    from fastapi import HTTPException
    
    @app.get("/", response_class=HTMLResponse)
    async def read_root():
        welcome_path = os.path.join(frontend_dir, "level_05_pages", "welcome.html")
        if os.path.exists(welcome_path):
            with open(welcome_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Welcome"

    @app.get("/{{page_name}}", response_class=HTMLResponse)
    async def read_page(page_name: str):
        if "." in page_name:
            raise HTTPException(status_code=404, detail="Not Found")
        file_name = page_name.replace("-", "_") + ".html"
        page_path = os.path.join(frontend_dir, "level_05_pages", file_name)
        if os.path.exists(page_path):
            with open(page_path, "r", encoding="utf-8") as f:
                return f.read()
        raise HTTPException(status_code=404, detail="Page not found")
        
    if os.path.exists(frontend_dir):
        app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")
        
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
"""
