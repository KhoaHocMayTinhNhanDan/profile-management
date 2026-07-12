from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.checkin_document.checkin_document_dto import (
    CheckinDocumentInput,
)
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/checkin-document", tags=["CheckinDocument"])


class CheckinDocumentRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


def get_context():
    return AppContextWeb()


@router.post("/")
async def checkin_document_endpoint(
    request: CheckinDocumentRequest, context: AppContextWeb = Depends(get_context)
):
    logger.info("Received request at CheckinDocument endpoint")
    controller = context.container.resolve("WebCheckinDocumentController")
    payload = request.data if request.data else {}
    try:
        response = await controller.execute(
            CheckinDocumentInput(
                profile_id=payload.get("profile_id", ""),
                document_id=payload.get("document_id", ""),
                user_id=payload.get("user_id", ""),
                new_url=payload.get("new_url", ""),
                new_size=payload.get("new_size", 0),
                new_checksum=payload.get("new_checksum", ""),
            )
        )
        if response.status == "success":
            return {"status": response.status, "message": response.message}
        raise HTTPException(status_code=400, detail=f"Failed: {response.message}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
