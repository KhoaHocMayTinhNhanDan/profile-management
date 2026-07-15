class DesktopTauriFactory:
    """
    Concrete Factory tạo các UI templates cho Desktop Tauri (Rust + HTML/JS).
    """

    def create_page(self, pascal_name: str, snake_name: str) -> str:
        # Tauri chia sẻ chung giao diện với web_fastapi frontend
        return ""

    def create_buttons(self) -> str:
        return ""

    def create_inputs(self) -> str:
        return ""

    def create_labels(self) -> str:
        return ""

    def create_async_hook(self) -> str:
        return ""

    def create_feature_hook(self, pascal_name: str, snake_name: str) -> str:
        return ""

    def create_cargo(self, project_name: str) -> str:
        return f"""[package]
name = "{project_name.lower()}-desktop"
version = "0.1.0"
description = "Tauri Desktop wrapper for {project_name}"
authors = ["Clean Architecture Kit"]
edition = "2021"

[build-dependencies]
tauri-build = {{ version = "1.5" }}

[dependencies]
tauri = {{ version = "1.5", features = ["shell-open"] }}
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"

[profile.release]
panic = "abort"
codegen-units = 1
lto = true
opt-level = "s"
strip = true
"""

    def create_tauri_conf(self, project_name: str) -> str:
        # Chúng ta trỏ devPath và distDir tới thư mục frontend tĩnh của web_fastapi
        return f"""{{
  "build": {{
    "beforeDevCommand": "",
    "beforeBuildCommand": "",
    "devPath": "http://localhost:8000",
    "distDir": "../../web_fastapi/frontend"
  }},
  "package": {{
    "productName": "{project_name}",
    "version": "0.1.0"
  }},
  "tauri": {{
    "allowlist": {{
      "all": false,
      "shell": {{
        "all": false,
        "open": true
      }}
    }},
    "bundle": {{
      "active": true,
      "targets": "all",
      "identifier": "com.cleanarch.{project_name.lower()}",
      "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
      ]
    }},
    "security": {{
      "csp": null
    }},
    "windows": [
      {{
        "title": "{project_name} - Desktop App",
        "width": 1024,
        "height": 768,
        "resizable": true,
        "fullscreen": false
      }}
    ]
  }}
}}
"""

    def create_main_rs(self) -> str:
        return """#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

fn main() {
  tauri::Builder::default()
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
"""
