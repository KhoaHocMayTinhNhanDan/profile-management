from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.update_profile.update_profile_dto import (
    UpdateProfileInput,
)
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/update-profile", tags=["UpdateProfile"])


class UpdateProfileRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


def get_context():
    return AppContextWeb()


@router.post("/")
async def update_profile_endpoint(
    request: UpdateProfileRequest, context: AppContextWeb = Depends(get_context)
):
    logger.info("Received request at UpdateProfile endpoint")
    controller = context.container.resolve("WebUpdateProfileController")
    payload = request.data if request.data else {}
    try:
        response = await controller.execute(
            UpdateProfileInput(
                profile_id=payload.get("profile_id", ""),
                dynamic_data=payload.get("dynamic_data", {}),
            )
        )
        if response.status == "success":
            return {"status": response.status, "message": response.message}
        raise HTTPException(status_code=400, detail=f"Failed: {response.message}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
