import logging
from logging.handlers import RotatingFileHandler
import pathlib


LOG_DIR = pathlib.Path('reports/logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    
    if not logger.handlers:
        
        fh = RotatingFileHandler(LOG_DIR / 'framework.log', maxBytes=5_000_000, backupCount=3, encoding='utf-8')
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        return logger
