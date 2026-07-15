class WebUiInspector:
    def get_template(self) -> str:
        return """(function() {
    if (window.WebUIInspector) return;

    const style = document.createElement('style');
    style.textContent = `
        .ui-inspector-hover-overlay {
            position: absolute;
            pointer-events: none;
            border: {{ BORDER_WIDTH }} dashed {{ ACCENT_COLOR }};
            background-color: rgba({{ ACCENT_COLOR_RGB }}, 0.1);
            z-index: 999999;
            transition: all calc(0.25 * {{ TRANSITION_DURATION }}) ease-out;
            display: none;
        }
        .ui-inspector-toast {
            position: fixed;
            bottom: calc(4 * {{ CARD_PADDING }});
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba({{ DARK_BG_RGB }}, 0.95);
            color: {{ SUCCESS_COLOR }};
            border: {{ BORDER_WIDTH }} solid {{ ACCENT_COLOR }};
            border-radius: {{ RADIUS }};
            padding: {{ INPUT_PADDING }};
            font-size: {{ STATUS_FONT_SIZE }};
            font-weight: bold;
            font-family: sans-serif;
            z-index: 1000000;
            opacity: 0;
            transition: opacity {{ TRANSITION_DURATION }} ease-in-out;
            pointer-events: none;
        }
    `;
    document.head.appendChild(style);

    const overlay = document.createElement('div');
    overlay.className = 'ui-inspector-hover-overlay';
    document.body.appendChild(overlay);

    const toast = document.createElement('div');
    toast.className = 'ui-inspector-toast';
    document.body.appendChild(toast);

    function showToast(msg) {
        toast.textContent = msg;
        toast.style.opacity = '1';
        if (msg.startsWith('❌')) {
            navigator.clipboard.writeText(msg).catch(() => {});
        }
        setTimeout(() => {
            toast.style.opacity = '0';
        }, 5000);
    }

    const state = {
        active: false,
        screenshotMode: false,
        singleScreenshotMode: false,
        hoveredEl: null
    };

    function updateOverlay(el, color = '{{ ACCENT_COLOR }}') {
        if (!el) {
            overlay.style.display = 'none';
            return;
        }
        const rect = el.getBoundingClientRect();
        const scrollX = window.scrollX || window.pageXOffset;
        const scrollY = window.scrollY || window.pageYOffset;
        overlay.style.border = `{{ BORDER_WIDTH }} dashed ${color}`;
        overlay.style.backgroundColor = color === '{{ ACCENT_COLOR }}' ? 'rgba({{ ACCENT_COLOR_RGB }}, 0.1)' : 'rgba({{ SUCCESS_COLOR_RGB }}, 0.1)';
        overlay.style.left = `${rect.left + scrollX}px`;
        overlay.style.top = `${rect.top + scrollY}px`;
        overlay.style.width = `${rect.width}px`;
        overlay.style.height = `${rect.height}px`;
        overlay.style.display = 'block';
    }

    function getElementPath(el) {
        let path = [];
        let curr = el;
        while (curr && curr !== document.body) {
            let name = curr.tagName.toLowerCase();
            if (curr.id) name += '#' + curr.id;
            let clsAttr = curr.getAttribute('class');
            if (clsAttr) {
                name += '.' + clsAttr.trim().split(/\\\\s+/).join('.');
            }
            path.push(name);
            curr = curr.parentElement;
        }
        return path.reverse().join(' -> ');
    }

    async function uploadScreenshot(dataUrl, filename, overwrite = false) {
        try {
            const res = await fetch('/api/v1/debug/save-screenshot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: dataUrl, filename: filename, overwrite: overwrite })
            });
            const data = await res.json();
            if (data.status === 'success') {
                showToast(`📸 ${data.message}`);
            } else {
                showToast(`❌ Error: ${data.message}`);
            }
        } catch (e) {
            console.error(e);
            showToast(`❌ Failed to send screenshot to dev server: ${e.message}`);
        }
    }

    function disableUnsupportedStylesheets() {
        const disabled = [];
        for (let i = 0; i < document.styleSheets.length; i++) {
            const sheet = document.styleSheets[i];
            try {
                if (!sheet.cssRules) continue;
                let hasUnsupported = false;
                for (let j = 0; j < sheet.cssRules.length; j++) {
                    const txt = sheet.cssRules[j].cssText;
                    if (txt.includes('oklch') || txt.includes('color-mix(') || txt.includes('oklab')) {
                        hasUnsupported = true;
                        break;
                    }
                }
                if (hasUnsupported) {
                    sheet.disabled = true;
                    disabled.push(sheet);
                }
            } catch (e) {
                // CORS or security restriction, ignore
            }
        }
        return disabled;
    }

    function restoreStylesheets(sheets) {
        for (const sheet of sheets) {
            sheet.disabled = false;
        }
    }

    const nativeGetComputedStyle = window.getComputedStyle;

    function enableStyleInterceptor() {
        window.getComputedStyle = function(el, pseudoElt) {
            const style = nativeGetComputedStyle(el, pseudoElt);
            return new Proxy(style, {
                get(target, prop) {
                    if (prop === 'getPropertyValue') {
                        return function(name) {
                            const val = target.getPropertyValue(name);
                            if (typeof val === 'string' && (val.includes('oklch') || val.includes('oklab') || val.includes('color-mix'))) {
                                return 'rgba(0,0,0,0)';
                            }
                            return val;
                        };
                    }
                    const val = target[prop];
                    if (typeof val === 'string' && (val.includes('oklch') || val.includes('oklab') || val.includes('color-mix'))) {
                        return 'rgba(0,0,0,0)';
                    }
                    if (typeof val === 'function') {
                        return val.bind(target);
                    }
                    return val;
                }
            });
        };
    }

    function disableStyleInterceptor() {
        window.getComputedStyle = nativeGetComputedStyle;
    }

    async function captureFullPage() {
        if (typeof html2canvas === 'undefined') {
            showToast("❌ Library html2canvas not loaded!");
            return;
        }
        const disabledSheets = disableUnsupportedStylesheets();
        enableStyleInterceptor();
        try {
            overlay.style.display = 'none';
            const canvas = await html2canvas(document.body);
            const dataUrl = canvas.toDataURL('image/png');
            await uploadScreenshot(dataUrl, 'ui_screenshot.png', true);
        } catch (err) {
            console.error(err);
            showToast(`❌ html2canvas error: ${err.message}`);
        } finally {
            disableStyleInterceptor();
            restoreStylesheets(disabledSheets);
        }
    }

    async function captureWidget(el, overwrite = false) {
        if (typeof html2canvas === 'undefined') {
            showToast("❌ Library html2canvas not loaded!");
            return;
        }
        const disabledSheets = disableUnsupportedStylesheets();
        enableStyleInterceptor();
        try {
            overlay.style.display = 'none';
            const canvas = await html2canvas(el);
            const dataUrl = canvas.toDataURL('image/png');
            
            let filename = 'widget_screenshot.png';
            if (!overwrite) {
                const className = el.className ? el.className.split(' ')[0].replace(/[^a-zA-Z0-9]/g, '') : 'element';
                filename = `web_mode_${el.tagName.toLowerCase()}_${className}.png`;
            }
            await uploadScreenshot(dataUrl, filename, overwrite);
        } catch (err) {
            console.error(err);
            showToast(`❌ html2canvas error: ${err.message}`);
        } finally {
            disableStyleInterceptor();
            restoreStylesheets(disabledSheets);
        }
    }

    document.addEventListener('mousemove', (e) => {
        if (!state.active && !state.screenshotMode && !state.singleScreenshotMode) return;
        const el = document.elementFromPoint(e.clientX, e.clientY);
        if (el && el !== overlay && el !== toast && el !== document.body && el !== document.documentElement) {
            state.hoveredEl = el;
            const color = (state.screenshotMode || state.singleScreenshotMode) ? '{{ SUCCESS_COLOR }}' : '{{ ACCENT_COLOR }}';
            updateOverlay(el, color);
        } else {
            state.hoveredEl = null;
            overlay.style.display = 'none';
        }
    });

    document.addEventListener('click', (e) => {
        if (!state.active && !state.screenshotMode && !state.singleScreenshotMode) return;
        e.preventDefault();
        e.stopPropagation();

        if (state.hoveredEl) {
            if (state.singleScreenshotMode) {
                captureWidget(state.hoveredEl, true);
            } else if (state.screenshotMode) {
                captureWidget(state.hoveredEl, false);
            } else if (state.active) {
                const path = getElementPath(state.hoveredEl);
                navigator.clipboard.writeText(path);
                showToast(`📋 Copied element path to clipboard!`);
                console.log("[UI Inspector Web]", path);
            }
        }
    }, true);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'F12') {
            e.preventDefault();
            state.active = !state.active;
            state.screenshotMode = false;
            state.singleScreenshotMode = false;
            overlay.style.display = 'none';
            showToast(state.active ? '🔌 Web UI Inspector ACTIVE (F12)' : '🔌 Web UI Inspector INACTIVE');
        } else if (e.key === 'F11') {
            e.preventDefault();
            captureFullPage();
        } else if (e.key === 'F10') {
            e.preventDefault();
            state.screenshotMode = !state.screenshotMode;
            state.active = false;
            state.singleScreenshotMode = false;
            overlay.style.display = 'none';
            showToast(state.screenshotMode ? '📸 Web Widget Snapshot ACTIVE (F10)' : '📸 Web Widget Snapshot INACTIVE');
        } else if (e.key === 'F9') {
            e.preventDefault();
            state.singleScreenshotMode = !state.singleScreenshotMode;
            state.active = false;
            state.screenshotMode = false;
            overlay.style.display = 'none';
            showToast(state.singleScreenshotMode ? '📸 Web Widget Overwrite ACTIVE (F9)' : '📸 Web Widget Overwrite INACTIVE');
        }
    });

    window.WebUIInspector = state;
    console.log("[UI Inspector Web] Loaded! Hotkeys: F9 (Single Widget), F10 (Widget Snapshots), F11 (Full App), F12 (Inspect)");
})();
"""
