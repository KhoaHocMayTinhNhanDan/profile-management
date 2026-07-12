from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.checkout_document.checkout_document_dto import (
    CheckoutDocumentInput,
)
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/checkout-document", tags=["CheckoutDocument"])


class CheckoutDocumentRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


def get_context():
    return AppContextWeb()


@router.post("/")
async def checkout_document_endpoint(
    request: CheckoutDocumentRequest, context: AppContextWeb = Depends(get_context)
):
    logger.info("Received request at CheckoutDocument endpoint")
    controller = context.container.resolve("WebCheckoutDocumentController")
    payload = request.data if request.data else {}
    try:
        response = await controller.execute(
            CheckoutDocumentInput(
                profile_id=payload.get("profile_id", ""),
                document_id=payload.get("document_id", ""),
                user_id=payload.get("user_id", ""),
            )
        )
        if response.status == "success":
            return {"status": response.status, "message": response.message}
        raise HTTPException(status_code=400, detail=f"Failed: {response.message}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
