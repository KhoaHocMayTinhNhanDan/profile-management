import { UpdateProfileController } from "../../../layer_03_interface_adapters/controllers/web/update_profile.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng UpdateProfile.
 */
export class UseUpdateProfile extends EventTarget {
    constructor() {
        super();
        this.loading = false;
        this.data = {};
    }
}
