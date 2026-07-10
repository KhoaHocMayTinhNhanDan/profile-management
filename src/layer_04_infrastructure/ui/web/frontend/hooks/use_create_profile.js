import { CreateProfileController } from "../../../layer_03_interface_adapters/controllers/web/create_profile.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng CreateProfile.
 */
export class UseCreateProfile extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
