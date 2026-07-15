from ..abstract.i_page_product import AbstractPage


class WebPage(AbstractPage):
    def get_template(self, pascal_name: str, snake_name: str) -> str:
        is_welcome = pascal_name == "Welcome"
        is_demo = pascal_name == "ColorPaletteDemo"

        if is_welcome:
            return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to {pascal_name}</title>
    <style>
        body {{
            background-color: {{ DARK_BG }};
            color: {{ TEXT_COLOR }};
            font-family: '{{ FONT_FAMILY }}';
            margin: 0;
            padding: calc(4 * {{ CARD_PADDING }});
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }}
        .container {{
            max-width: {{ CONTAINER_MAX_WIDTH }};
            width: 100%;
        }}
        h1 {{
            color: {{ ACCENT_COLOR }};
            font-size: calc(2.2 * {{ HEADER_FONT_SIZE }});
            margin-bottom: {{ SPACING_BASE }};
            text-align: center;
        }}
        .subtitle {{
            color: {{ SUBTEXT_COLOR }};
            font-size: {{ HEADER_FONT_SIZE }};
            margin-bottom: calc(4 * {{ CARD_PADDING }});
            text-align: center;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax({{ GRID_MIN_WIDTH }}, 1fr));
            gap: calc(2 * {{ CARD_PADDING }});
            margin-bottom: calc(4 * {{ CARD_PADDING }});
        }}
        .card {{
            background-color: {{ CARD_BG }};
            border: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            border-radius: {{ RADIUS }};
            padding: calc(2.4 * {{ CARD_PADDING }});
            box-shadow: {{ SHADOW }};
            transition: transform {{ TRANSITION_DURATION }} ease, border-color {{ TRANSITION_DURATION }} ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
            border-color: {{ ACCENT_COLOR }};
        }}
        .card h2 {{
            color: {{ ACCENT_HOVER }};
            font-size: {{ HEADER_FONT_SIZE }};
            margin-top: 0;
            margin-bottom: calc(1.2 * {{ CARD_PADDING }});
            display: flex;
            align-items: center;
            gap: calc(1 * {{ CARD_PADDING }});
        }}
        .card p {{
            color: {{ TEXT_COLOR }};
            font-size: {{ BODY_FONT_SIZE }};
            line-height: 1.6;
            margin: 0;
        }}
        .footer {{
            text-align: center;
            font-weight: bold;
            color: {{ SUCCESS_COLOR }};
            font-size: {{ BODY_FONT_SIZE }};
            margin-top: calc(2 * {{ CARD_PADDING }});
            border-top: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            padding-top: calc(2.5 * {{ CARD_PADDING }});
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>WELCOME TO {pascal_name}</h1>
        <div class="subtitle">Clean Architecture client scaffolded successfully with HTML5 / Web Components.</div>
        
        <div class="grid">
            <div class="card">
                <h2>🛡️ Layer 01 - Entities</h2>
                <p>Pure domain logic, data models, entities and validation rules. Free of framework dependencies.</p>
            </div>
            <div class="card">
                <h2>⚡ Layer 02 - Use Cases</h2>
                <p>Application specific business workflows. Contains interactors, DTOs, and gateway interfaces.</p>
            </div>
            <div class="card">
                <h2>🔌 Layer 03 - Adapters</h2>
                <p>Adapts data models between UI and business layers. Contains presenters, controllers and gateways.</p>
            </div>
            <div class="card">
                <h2>🌐 Layer 04 - Infrastructure</h2>
                <p>All concrete implementations: Web Components UI pages, local API routes, and web fetch drivers.</p>
            </div>
        </div>
        
        <div class="card" style="margin-top: calc(2 * {{ CARD_PADDING }}); margin-bottom: calc(2 * {{ CARD_PADDING }});">
            <h2 style="color: {{ SUCCESS_COLOR }}; font-size: {{ HEADER_FONT_SIZE }}; margin-top: 0; margin-bottom: calc(1.2 * {{ CARD_PADDING }}); display: flex; align-items: center; gap: calc(1 * {{ CARD_PADDING }});">🚀 Active Screen Pages (Sinh Tự Động)</h2>
            <div id="pages-list" style="display: flex; flex-direction: column; gap: 10px; padding: 5px 0;">
                <p style="color: {{ SUBTEXT_COLOR }}; font-size: {{ BODY_FONT_SIZE }}; margin: 0;">Đang tải danh sách các màn hình...</p>
            </div>
        </div>
        
        <div class="footer">
            👉 <a href="/color-palette-demo" style="color: {{ SUCCESS_COLOR }}; text-decoration: underline; font-weight: bold;">Go to Color Palette Demo Page</a> to run mock simulations.
        </div>
    </div>

    <!-- Thư viện chụp ảnh màn hình cho Web -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <!-- UI INSPECTOR FOR CLEAN ARCHITECTURE DEVELOPERS -->
    <script src="../level_02_molecules/ui_inspector/ui_inspector.js" defer></script>
    
    <script>
        async function loadPages() {{
            try {{
                const res = await fetch("/api/v1/debug/pages");
                const data = await res.json();
                const container = document.getElementById("pages-list");
                if (data.pages && data.pages.length > 0) {{
                    container.innerHTML = "";
                    data.pages.forEach(p => {{
                        const link = document.createElement("a");
                        link.href = p.route;
                        link.style.color = "{{ ACCENT_HOVER }}";
                        link.style.textDecoration = "underline";
                        link.style.fontSize = "14px";
                        link.style.fontWeight = "bold";
                        link.textContent = `👉 Mở màn hình: ${{p.name}} (${{p.route}})`;
                        container.appendChild(link);
                    }});
                }} else {{
                    container.innerHTML = `<p style="color: {{ SUBTEXT_COLOR }}; font-size: {{ BODY_FONT_SIZE }}; margin: 0;">Chưa có màn hình tính năng nào được sinh. Hãy dùng Project Manager App để sinh thêm tính năng!</p>`;
                }}
            }} catch (e) {{
                document.getElementById("pages-list").innerHTML = `<p style="color: {{ ERROR_COLOR }}; font-size: {{ BODY_FONT_SIZE }}; margin: 0;">Không thể kết nối đến debug API.</p>`;
            }}
        }}
        loadPages();
    </script>
</body>
</html>
"""

        if is_demo:
            return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Color Harmony Verification</title>
    <style>
        body {{
            background-color: {{ DARK_BG }};
            color: {{ TEXT_COLOR }};
            font-family: '{{ FONT_FAMILY }}';
            margin: 0;
            padding: calc(3 * {{ CARD_PADDING }});
            box-sizing: border-box;
        }}
        .top-section {{
            display: flex;
            align-items: center;
            gap: calc(1.5 * {{ CARD_PADDING }});
            margin-bottom: calc(2.5 * {{ CARD_PADDING }});
            flex-wrap: wrap;
        }}
        select, button {{
            background-color: {{ CARD_BG }};
            color: {{ TEXT_COLOR }};
            border: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            border-radius: {{ RADIUS }};
            padding: {{ INPUT_PADDING }};
            font-size: {{ INPUT_FONT_SIZE }};
            outline: none;
            cursor: pointer;
        }}
        select:focus, button:hover {{
            border-color: {{ ACCENT_COLOR }};
        }}
        .status-box {{
            margin-left: auto;
            display: flex;
            gap: calc(1.5 * {{ CARD_PADDING }});
            font-size: {{ STATUS_FONT_SIZE }};
            color: {{ SUBTEXT_COLOR }};
        }}
        .status-dot {{
            color: {{ SUCCESS_COLOR }};
            font-weight: bold;
        }}
        .middle-section {{
            display: flex;
            gap: calc(2 * {{ CARD_PADDING }});
            margin-bottom: calc(2.5 * {{ CARD_PADDING }});
            flex-wrap: wrap;
        }}
        .card {{
            background-color: {{ CARD_BG }};
            border: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            border-radius: {{ RADIUS }};
            padding: {{ CARD_PADDING }};
            box-shadow: {{ SHADOW }};
        }}
        .card h3 {{
            margin-top: 0;
            margin-bottom: {{ LABEL_MARGIN_BOTTOM }};
            font-size: {{ HEADER_FONT_SIZE }};
            color: {{ ACCENT_HOVER }};
        }}
        .info-card {{
            flex: 1;
            min-width: 250px;
        }}
        .selection-card {{
            flex: 2;
            min-width: 350px;
        }}
        .grid-options {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: calc(2 * {{ SPACING_BASE }});
        }}
        .option-item {{
            display: flex;
            align-items: center;
            gap: calc(2 * {{ SPACING_BASE }});
            font-size: {{ BODY_FONT_SIZE }};
        }}
        .control-section {{
            margin-bottom: calc(2.5 * {{ CARD_PADDING }});
        }}
        .progress-bar-container {{
            background-color: {{ BORDER_COLOR }};
            border-radius: {{ PROGRESS_RADIUS }};
            height: {{ PROGRESS_HEIGHT }};
            overflow: hidden;
            margin-bottom: calc(1.5 * {{ CARD_PADDING }});
        }}
        .progress-bar-fill {{
            background-color: {{ ACCENT_COLOR }};
            height: 100%;
            width: 0%;
            transition: width calc(0.5 * {{ TRANSITION_DURATION }}) linear;
        }}
        .stats-row {{
            display: flex;
            justify-content: space-between;
            font-size: {{ STATUS_FONT_SIZE }};
            color: {{ SUBTEXT_COLOR }};
            margin-bottom: calc(1.5 * {{ CARD_PADDING }});
        }}
        .btn-group {{
            display: flex;
            gap: calc(2 * {{ SPACING_BASE }});
        }}
        .btn-start {{ background-color: rgba({{ SUCCESS_COLOR_RGB }}, 0.15); color: {{ SUCCESS_COLOR }}; border-color: {{ SUCCESS_COLOR }}; }}
        .btn-pause {{ background-color: rgba({{ ACCENT_HOVER_RGB }}, 0.15); color: {{ ACCENT_HOVER }}; border-color: {{ ACCENT_HOVER }}; }}
        .btn-abort {{ background-color: rgba({{ ERROR_COLOR_RGB }}, 0.15); color: {{ ERROR_COLOR }}; border-color: {{ ERROR_COLOR }}; }}
        .btn-start:hover {{ background-color: {{ SUCCESS_COLOR }}; color: {{ SIDEBAR_BG }}; }}
        .btn-pause:hover {{ background-color: {{ ACCENT_HOVER }}; color: {{ SIDEBAR_BG }}; }}
        .btn-abort:hover {{ background-color: {{ ERROR_COLOR }}; color: {{ SIDEBAR_BG }}; }}
        .console {{
            background-color: {{ SIDEBAR_BG }};
            color: {{ SUCCESS_COLOR }};
            border: {{ BORDER_WIDTH }} solid {{ BORDER_COLOR }};
            border-radius: {{ CONSOLE_RADIUS }};
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: {{ CONSOLE_FONT_SIZE }};
            padding: {{ CONSOLE_PADDING }};
            height: {{ CONSOLE_HEIGHT }};
            overflow-y: auto;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <div class="top-section">
        <select id="mode-select">
            <option>Contrast & Color Verification</option>
            <option>Responsive Grid Layout Check</option>
            <option>Widget State Render Test</option>
        </select>
        <button id="theme-toggle">🌙 Dark Mode</button>
        
        <div class="status-box">
            <span>● WebLink: <span class="status-dot">Connected</span></span>
            <span>● Service: <span class="status-dot">Ready</span></span>
        </div>
    </div>

    <div class="middle-section">
        <div class="card info-card">
            <h3>Design Spec: Color Harmony Verification</h3>
            <p style="font-size: {{ BODY_FONT_SIZE }}; line-height: 1.5; margin: 0; color: {{ TEXT_COLOR }};">
                Verify color harmony across all elements:<br>
                - Background: Slate Dark ({{ DARK_BG }})<br>
                - Sidebar: Dark Panel ({{ SIDEBAR_BG }})<br>
                - Accents: Pink / Mauve ({{ ACCENT_HOVER }} / {{ ACCENT_COLOR }})<br>
                - Statuses: Green / Yellow / Red
            </p>
        </div>
        <div class="card selection-card">
            <h3>VERIFIABLE ELEMENT STATES</h3>
            <div class="grid-options">
                <div class="option-item"><input type="checkbox" checked id="opt1"> <label for="opt1">Primary Colors</label></div>
                <div class="option-item"><input type="checkbox" checked id="opt2"> <label for="opt2">Secondary Accent</label></div>
                <div class="option-item"><input type="checkbox" checked id="opt3"> <label for="opt3">States Hover/Active</label></div>
                <div class="option-item"><input type="checkbox" checked id="opt4"> <label for="opt4">Contrast Accessibility</label></div>
            </div>
        </div>
    </div>

    <div class="control-section">
        <div class="progress-bar-container">
            <div class="progress-bar-fill" id="progress-fill"></div>
        </div>
        <div class="stats-row">
            <span id="speed-label">Speed: -- MB/s</span>
            <span id="eta-label">Remaining: --</span>
        </div>
        <div class="btn-group">
            <button class="btn-start" id="btn-start">Start Palette Test</button>
            <button class="btn-pause" id="btn-pause" disabled>Pause</button>
            <button class="btn-abort" id="btn-abort" disabled>Abort</button>
        </div>
    </div>

    <h3 style="font-size: {{ HEADER_FONT_SIZE }}; color: {{ SUBTEXT_COLOR }}; margin-bottom: {{ LABEL_MARGIN_BOTTOM }};">REALTIME PALETTE RENDER LOGS</h3>
    <div class="console" id="console-logs">[READY] Color presets successfully loaded. Press 'Start Palette Test' to verify render flows...</div>

    <script>
        const btnStart = document.getElementById('btn-start');
        const btnPause = document.getElementById('btn-pause');
        const btnAbort = document.getElementById('btn-abort');
        const progressFill = document.getElementById('progress-fill');
        const speedLabel = document.getElementById('speed-label');
        const etaLabel = document.getElementById('eta-label');
        const consoleLogs = document.getElementById('console-logs');
        const themeToggle = document.getElementById('theme-toggle');

        let interval = null;
        let progress = 0;
        let isPaused = false;
        let logStep = 0;

        const logs = [
            "[INFO] Initiating palette rendering context...",
            "[RENDER] Drawing Background nodes with DARK_BG ({{ DARK_BG }})...",
            "[RENDER] Drawing Sidebar panel using SIDEBAR_BG ({{ SIDEBAR_BG }})...",
            "[RENDER] PrimaryButton active state contrast verified (Ratio 4.8:1).",
            "[RENDER] Text element colors loaded cleanly.",
            "[SUCCESS] Color presets rendering simulation complete."
        ];

        function log(msg) {{
            consoleLogs.textContent += "\\n" + msg;
            consoleLogs.scrollTop = consoleLogs.scrollHeight;
        }}

        btnStart.addEventListener('click', () => {{
            btnStart.disabled = true;
            btnPause.disabled = false;
            btnAbort.disabled = false;
            progress = 0;
            logStep = 0;
            isPaused = false;
            consoleLogs.textContent = "[INFO] Starting color palette verification test...";
            
            interval = setInterval(() => {{
                if (isPaused) return;
                
                if (progress < 100) {{
                    progress += 2;
                    progressFill.style.width = progress + '%';
                    
                    const speed = (40.0 + (Math.random() * 6 - 3)).toFixed(1);
                    speedLabel.textContent = `Speed: ${{speed}} MB/s`;
                    
                    const remaining = Math.ceil((100 - progress) * 0.25);
                    etaLabel.textContent = `Remaining: ${{remaining}}s`;
                    
                    if (progress % 16 === 0 && logStep < logs.length) {{
                        log(logs[logStep++]);
                    }}
                }} else {{
                    clearInterval(interval);
                    speedLabel.textContent = "Speed: 0.0 MB/s";
                    etaLabel.textContent = "Remaining: Done";
                    btnPause.disabled = true;
                    btnAbort.disabled = true;
                    btnStart.disabled = false;
                    alert("Color palette verification test completed successfully!");
                }}
            }}, 200);
        }});

        btnPause.addEventListener('click', () => {{
            isPaused = !isPaused;
            btnPause.textContent = isPaused ? "Resume" : "Pause";
            log(isPaused ? "[WARN] Color palette verification test paused." : "[INFO] Color palette verification test resumed.");
        }});

        btnAbort.addEventListener('click', () => {{
            clearInterval(interval);
            progress = 0;
            progressFill.style.width = '0%';
            speedLabel.textContent = "Speed: -- MB/s";
            etaLabel.textContent = "Remaining: --";
            btnStart.disabled = false;
            btnPause.disabled = true;
            btnAbort.disabled = true;
            btnPause.textContent = "Pause";
            log("[ERROR] Color palette verification test aborted.");
        }});

        let isDark = true;
        themeToggle.addEventListener('click', () => {{
            isDark = !isDark;
            document.body.style.backgroundColor = isDark ? '{{ DARK_BG }}' : '{{ LIGHT_BG }}';
            document.body.style.color = isDark ? '{{ TEXT_COLOR }}' : '{{ LIGHT_TEXT }}';
            themeToggle.textContent = isDark ? "🌙 Dark Mode" : "☀️ Light Mode";
        }});
    </script>

    <!-- Thư viện chụp ảnh màn hình cho Web -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <!-- UI INSPECTOR FOR CLEAN ARCHITECTURE DEVELOPERS -->
    <script src="../level_02_molecules/ui_inspector/ui_inspector.js" defer></script>
</body>
</html>
"""

        return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Màn hình {pascal_name}</title>
</head>
<body style="background-color: {{ DARK_BG }}; padding: calc(3 * {{ CARD_PADDING }}); font-family: '{{ FONT_FAMILY }}'; color: {{ TEXT_COLOR }};">
    <h1>Màn hình {pascal_name}</h1>
    <p>Trang {pascal_name} đã sẵn sàng cho giao diện tùy chỉnh của bạn.</p>

    <!-- Thư viện chụp ảnh màn hình cho Web -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <!-- UI INSPECTOR FOR CLEAN ARCHITECTURE DEVELOPERS -->
    <script src="../level_02_molecules/ui_inspector/ui_inspector.js" defer></script>
</body>
</html>
"""
