class CliFactory:
    """
    Concrete Factory cho CLI commands.
    """

    @staticmethod
    def get_ui_cli_template(pascal_name: str, snake_name: str) -> str:
        return f"""import argparse
import asyncio
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)

async def run_cli_async():
    logger.info("--- Starting {pascal_name} CLI ---")
    parser = argparse.ArgumentParser(description="Chạy tính năng {pascal_name}")
    args = parser.parse_args()
    
    # context = AppContextCLI(...)
    # controller = context.container.resolve("Cli{pascal_name}Controller")
    # await controller.execute(...)
    logger.info("Đã gọi tính năng {pascal_name} qua CLI.")

def run_cli():
    asyncio.run(run_cli_async())

if __name__ == "__main__":
    run_cli()
"""
