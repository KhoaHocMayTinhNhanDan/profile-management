import { CheckinDocumentController } from "../../../layer_03_interface_adapters/controllers/web/checkin_document.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CheckinDocument.
 */
export class UseCheckinDocument extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
