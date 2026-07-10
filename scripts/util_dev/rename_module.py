#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility script to rename or move Python modules/packages and automatically fix all import statements across the project.
Powered by Rope refactoring library.

Usage:
    python scripts/util_dev/rename_module.py <target_path> <new_name>
"""

import sys
import os

try:
    from rope.base.project import Project
    from rope.refactor.rename import Rename
except ImportError:
    print("[ERROR] 'rope' library is not installed in the virtual environment.")
    print("Please run: pip install rope")
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/util_dev/rename_module.py <target_path> <new_name>")
        print("Example: python scripts/util_dev/rename_module.py src/layer_01_entities/old_name.py new_name")
        sys.exit(1)

    target_path = sys.argv[1]
    new_name = sys.argv[2]

    if not os.path.exists(target_path):
        print(f"[ERROR] Target path '{target_path}' does not exist.")
        sys.exit(1)

    # Initialize rope project at workspace root
    print("Initializing refactoring project...")
    project = Project(".")

    try:
        # Get resource object for target path
        resource = project.get_resource(target_path)

        print(f"Refactoring: Renaming '{target_path}' to '{new_name}'...")
        refactor = Rename(project, resource)

        # Generate change details and apply
        changes = refactor.get_changes(new_name)
        project.do(changes)

        print("[SUCCESS] Refactoring completed successfully! All imports have been auto-fixed.")
    except Exception as e:
        print(f"[ERROR] Refactoring failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
