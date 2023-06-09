import logging

logger = logging.getLogger(__name__)


def error_log(message: str) -> None:
    logger.error(message)


def debug_log(message: str) -> None:
    logger.debug(message)


def warning_log(message: str) -> None:
    logger.warning(message)


def info_log(message: str) -> None:
    logger.info(message)


def critical_log(message: str) -> None:
    logger.critical(message)
