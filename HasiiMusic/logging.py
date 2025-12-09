import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "log.txt"
LOG_LEVEL = logging.INFO

FORMAT = "[%(asctime)s - %(levelname)s] - %(name)s - %(message)s"
DATEFMT = "%d-%b-%y %H:%M:%S"

logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    datefmt=DATEFMT,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler(
            LOG_FILE,
            maxBytes=10_000_000,
            backupCount=3,
            encoding="utf-8"
        ),
    ],
)

# Gürültü yapan kütüphanelerin log seviyesini düşür
for lib, level in [
    ("httpx", logging.ERROR),
    ("pyrogram", logging.ERROR),
    ("pytgcalls", logging.ERROR),
    ("pymongo", logging.ERROR),
    ("ntgcalls", logging.CRITICAL),
]:
    logging.getLogger(lib).setLevel(level)


# ✅ SABİT LOGGER — bunu import edip .info() kullanıyorsun
LOGGER = logging.getLogger("HasiiMusic")


# (İsteğe bağlı) modül bazlı logger almak isteyenler için
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
