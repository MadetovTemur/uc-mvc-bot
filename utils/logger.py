import logging
import sys

logger = logging.getLogger("uc_shop_bot")
logger.setLevel(logging.INFO)

if not logger.handlers:
    _fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setFormatter(_fmt)
    logger.addHandler(_stream_handler)

    _file_handler = logging.FileHandler("bot.log", encoding="utf-8")
    _file_handler.setFormatter(_fmt)
    logger.addHandler(_file_handler)
