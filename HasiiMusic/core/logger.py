# HasiiMusic/core/logger.py
import logging
import sys

LOGGER = logging.getLogger("HasiiMusic")
if not LOGGER.handlers:
    LOGGER.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s - %(levelname)s] - %(message)s")
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)
