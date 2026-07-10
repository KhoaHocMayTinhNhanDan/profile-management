/**
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
