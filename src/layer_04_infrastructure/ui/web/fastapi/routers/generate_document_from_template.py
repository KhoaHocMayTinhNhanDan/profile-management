from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.shared.logger.app_logger import get_logger

from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_dto import (
    GenerateDocumentFromTemplateInput,
)
from src.layer_05_bootstrap.app_context_web import AppContextWeb

logger = get_logger(__name__)
router = APIRouter(
    prefix="/api/v1/generate-document-from-template",
    tags=["GenerateDocumentFromTemplate"],
)


class GenerateDocumentFromTemplateRequest(BaseModel):
    data: Optional[Dict[str, Any]] = None


def get_context():
    return AppContextWeb()


@router.post("/")
async def generate_document_from_template_endpoint(
    request: GenerateDocumentFromTemplateRequest,
    context: AppContextWeb = Depends(get_context),
):
    logger.info("Received request at GenerateDocumentFromTemplate endpoint")
    controller = context.container.resolve("WebGenerateDocumentFromTemplateController")
    payload = request.data if request.data else {}
    try:
        response = await controller.execute(
            GenerateDocumentFromTemplateInput(
                profile_id=payload.get("profile_id", ""),
                template_doc_path=payload.get("template_doc_path", ""),
                output_doc_name=payload.get("output_doc_name", ""),
            )
        )
        if response.status == "success":
            return {"status": response.status, "message": response.message}
        raise HTTPException(status_code=400, detail=f"Failed: {response.message}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
