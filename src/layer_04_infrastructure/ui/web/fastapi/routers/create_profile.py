from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.create_profile.create_profile_dto import CreateProfileInput
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/create-profile", tags=["CreateProfile"])

class CreateProfileRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None

def get_context():
    return AppContextWeb()

@router.post("/")
async def create_profile_endpoint(request: CreateProfileRequest, context: AppContextWeb = Depends(get_context)):
    logger.info("Received request at CreateProfile endpoint")
    controller = context.container.resolve("WebCreateProfileController")
    payload = request.data if request.data else {}
    try:
        response = await controller.execute(CreateProfileInput(
            profile_id=payload.get("profile_id", ""),
            template_id=payload.get("template_id", ""),
            dynamic_data=payload.get("dynamic_data", {})
        ))
        if response.status == "success":
            return {"status": response.status, "message": response.message}
        raise HTTPException(status_code=400, detail=f"Failed: {response.message}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
