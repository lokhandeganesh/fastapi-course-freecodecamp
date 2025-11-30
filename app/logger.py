from loguru import logger
import sys
import os

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

logger.remove()  # Remove default log handler

# INFO log (includes DEBUG, INFO, WARNING — excludes ERROR)
logger.add("logs/info.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="INFO",
    filter=lambda record: record["level"].name != "ERROR")

# ERROR log (includes only ERROR and above)
logger.add("logs/error.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    level="ERROR")

# Optional: Also log to console
logger.add(sys.stderr, level="INFO")
