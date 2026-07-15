import unittest
import tempfile
import os
import json
from scripts.util_dev.project_manager_app.config.project_config import (
    read_project_name,
    read_project_branding,
    write_project_name,
    clear_project_config,
)


class TestProjectConfig(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.root_dir = self.test_dir.name

    def tearDown(self):
        self.test_dir.cleanup()

    def test_read_non_existent_config(self):
        self.assertEqual(read_project_name(self.root_dir), "")
        self.assertEqual(read_project_branding(self.root_dir), {})

    def test_write_and_read_project_name(self):
        success = write_project_name(self.root_dir, "MySpaceship")
        self.assertTrue(success)
        self.assertEqual(read_project_name(self.root_dir), "MySpaceship")

    def test_preserve_branding_on_write_project_name(self):
        config_dir = os.path.join(
            self.root_dir,
            ".projects",
        )
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "project_config.json")

        branding_data = {
            "accent_color_dark": "#ff007f",
            "accent_hover_dark": "#ff3399",
            "accent_color_light": "#e0115f",
            "accent_hover_light": "#b80f40",
            "font_family": "Courier New, monospace",
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump({"project_name": "OldName", "branding": branding_data}, f)

        success = write_project_name(self.root_dir, "NewName")
        self.assertTrue(success)

        self.assertEqual(read_project_name(self.root_dir), "NewName")
        self.assertEqual(read_project_branding(self.root_dir), branding_data)

    def test_clear_project_config(self):
        write_project_name(self.root_dir, "TempProject")
        self.assertEqual(read_project_name(self.root_dir), "TempProject")

        success = clear_project_config(self.root_dir)
        self.assertTrue(success)

        self.assertEqual(read_project_name(self.root_dir), "")


if __name__ == "__main__":
    unittest.main()
