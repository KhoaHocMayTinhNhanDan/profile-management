import { GenerateDocumentFromTemplateController } from "../../../layer_03_interface_adapters/controllers/web/generate_document_from_template.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng GenerateDocumentFromTemplate.
 */
export class UseGenerateDocumentFromTemplate extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
