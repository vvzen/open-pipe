import os
import logging


class LoggerCache(object):
    """
    Singleton cache for storing and retrieving loggers
    """

    _cache = {}

    @classmethod
    def get(cls, name):
        return cls._cache.get(name)

    @classmethod
    def set(cls, name, logger):
        cls._cache[name] = logger

    @classmethod
    def clear(cls):
        cls._cache = {}


def get_logger(name):
    """Retrieve a logger with a specific name

    :param name: name of the logger
    :type name: str
    :return: the logger, if found, or a new one with that name
    :rtype: logging.Logger
    """

    logger = LoggerCache.get(name)
    if logger:
        return logger

    logger = logging.getLogger(name)
    level = logging.INFO
    formatter_string = ("%(asctime)s: %(message)s")

    if os.getenv("OPENPIPE_LOG") == "DEBUG":
        level = logging.DEBUG
        formatter_string = ("%(asctime)s-%(filename)s:"
                            "%(lineno)s@%(funcName)s() : %(message)s")

    logger.setLevel(level)

    formatter = logging.Formatter(formatter_string)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    LoggerCache.set(name, logger)

    return logger
