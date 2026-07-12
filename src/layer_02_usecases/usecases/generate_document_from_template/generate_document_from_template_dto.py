from dataclasses import dataclass


@dataclass
class GenerateDocumentFromTemplateInput:
    profile_id: str
    template_doc_path: (
        str  # Path to template docx containing placeholders like {{full_name}}
    )
    output_doc_name: str  # e.g., "HD_Nhan_Su.docx"


@dataclass
class GenerateDocumentFromTemplateOutput:
    status: str
    message: str
    document_id: str = ""
    document_url: str = ""
