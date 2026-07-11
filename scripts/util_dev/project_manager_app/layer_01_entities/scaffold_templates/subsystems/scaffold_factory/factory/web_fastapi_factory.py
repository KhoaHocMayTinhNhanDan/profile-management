class WebFastApiFactory:
    """
    Concrete Factory tạo router backend FastAPI.
    """

    @staticmethod
    def get_fastapi_router_template(pascal_name: str, snake_name: str) -> str:
        kebab = snake_name.replace("_", "-")
        return f"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.{snake_name}.{snake_name}_dto import {pascal_name}Input
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
    controller = context.container.resolve("Web{pascal_name}Controller")
    payload = request.data if request.data else {{}}
    try:
        response = await controller.execute({pascal_name}Input())
        if response.status == "success":
            return {{"status": response.status, "message": response.message}}
        raise HTTPException(status_code=400, detail=f"Failed: {{response.message}}")
    except ValueError as e:
        logger.error(f"Validation error: {{str(e)}}")
        raise HTTPException(status_code=400, detail=str(e))
"""
