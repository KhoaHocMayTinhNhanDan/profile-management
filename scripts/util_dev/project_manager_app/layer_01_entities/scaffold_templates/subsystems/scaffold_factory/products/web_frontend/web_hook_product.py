from ..abstract.i_hook_product import AbstractHook


class WebHook(AbstractHook):
    def get_async_template(self) -> str:
        return """/**
 * Custom Hook tổng quát hóa hỗ trợ chạy bất đồng bộ mọi tác vụ IO/CPU nặng trên Web Frontend.
 */
export class UseAsync extends EventTarget {
    constructor() {
        super();
        this.loading = false;
    }

    async execute(asyncFn, ...args) {
        if (this.loading) return false;
        this.loading = true;
        this.dispatchEvent(new CustomEvent("loading", { detail: true }));

        try {
            const res = await asyncFn(...args);
            this.dispatchEvent(new CustomEvent("finished", { detail: { success: true, result: res, errorMsg: "" } }));
            return true;
        } catch (err) {
            this.dispatchEvent(new CustomEvent("finished", { detail: { success: false, result: null, errorMsg: err.message } }));
            return false;
        } finally {
            this.loading = false;
            this.dispatchEvent(new CustomEvent("loading", { detail: false }));
        }
    }
}
"""

    def get_feature_template(self, pascal_name: str, snake_name: str) -> str:
        return f"""import {{ {pascal_name}Controller }} from "../../../layer_03_interface_adapters/controllers/web/{snake_name}.js";

/**
 * Custom Hook quản lý trạng thái hiển thị và luồng công việc cho tính năng {pascal_name}.
 */
export class Use{pascal_name} extends EventTarget {{
    constructor() {{
        super();
        this.loading = false;
        this.data = {{}};
    }}
}}
"""
