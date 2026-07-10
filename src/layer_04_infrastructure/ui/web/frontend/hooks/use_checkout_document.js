import { CheckoutDocumentController } from "../../../layer_03_interface_adapters/controllers/web/checkout_document.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CheckoutDocument.
 */
export class UseCheckoutDocument extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
