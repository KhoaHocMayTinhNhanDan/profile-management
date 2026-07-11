import sys
import os

# Add project root to python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")
    ),
)

from scripts.util_dev.project_manager_app.layer_04_infrastructure.ui.cli.main import (
    main,
)

if __name__ == "__main__":
    main()
