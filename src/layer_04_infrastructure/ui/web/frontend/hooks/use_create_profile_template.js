import { CreateProfileTemplateController } from "../../../layer_03_interface_adapters/controllers/web/create_profile_template.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CreateProfileTemplate.
 */
export class UseCreateProfileTemplate extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
