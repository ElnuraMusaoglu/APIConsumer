import logging


def init_logging():
    logging.basicConfig(level=logging.INFO)


def info(msg: str):
    logging.info(msg)
