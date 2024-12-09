# logger.py

import logging
import json
from datetime import datetime
from config import LOG_FILE
from database import log_message_to_db


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_record)


logger = logging.getLogger("trading_logger")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)


def log_trade(trade_info):
    logger.info(f"Trade Executed: {trade_info}")
    log_message_to_db("INFO", f"Trade Executed: {trade_info}")


def log_message(level, message):
    if level.upper() == "INFO":
        logger.info(message)
    elif level.upper() == "ERROR":
        logger.error(message)
    elif level.upper() == "WARNING":
        logger.warning(message)
    else:
        logger.debug(message)
    log_message_to_db(level.upper(), message)
