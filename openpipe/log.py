import os
import logging

LOGGING_LEVELS_AS_STRINGS = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL"]


def user_requested_custom_logging_level():
    """Check if we are required to use a specific logging level.
    If that's the case, return it.

    :return: the logging level requested
    :rtype: None or int
    """

    # EG: export OPENPIPE_LOG=DEBUG

    env_var = os.getenv("OPENPIPE_LOG", "")
    if not env_var:
        return

    for level in LOGGING_LEVELS_AS_STRINGS:
        if level in env_var:
            return getattr(logging, level)


def user_requested_custom_formatting():
    """Check if we are required to use a specific formatting string.
    If that's the case, return it.

    :return: the formatting string requested
    :rtype: None or str
    """
    # EG: export OPENPIPE_LOG="DEBUG %(asctime)s-%(filename)s:"

    env_var = os.getenv("OPENPIPE_LOG")
    if not env_var:
        return

    tokens = env_var.split(" ")
    if not tokens:
        return

    num_tokens = len(tokens)

    if tokens[num_tokens-1] in LOGGING_LEVELS_AS_STRINGS:
        return

    return tokens[num_tokens-1]


class CustomFormatter(logging.Formatter):

    # These are the ANSI escape sequences needed to get colored ouput
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    # For more info, see https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    black, red, green, yellow, blue, magenta, cyan, white = \
        [30 + n for n in range(8)]

    # To test this code, run something like:
    # print(COLOR_SEQ % (30 + RED) + "hello" + RESET_SEQ)

    def __init__(self):
        formatter_string = ("%(asctime)s: %(message)s")

        # Use the provided formatting, if the user asked for it
        custom_formatting = user_requested_custom_formatting()
        if custom_formatting:
            formatter_string = custom_formatting
        # If we're debugging and nothing custom was asked, use something a bit
        # more descriptive anyway
        user_level = user_requested_custom_logging_level()
        if user_level == logging.DEBUG:
            formatter_string = ("%(asctime)s-%(filename)s:"
                                "%(lineno)s@%(funcName)s() : %(message)s")

        colors_map = {
            logging.DEBUG: self.blue,
            logging.INFO: self.green,
            logging.WARNING: self.yellow,
            logging.ERROR: self.red,
            logging.CRITICAL: self.magenta,
        }

        self.FORMATS = {}
        for level, _fmt in colors_map.items():
            self.FORMATS[level] = \
                (self.COLOR_SEQ % _fmt) + formatter_string + self.RESET_SEQ


    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    """Retrieve a logger with a specific name

    :param name: name of the logger
    :type name: str
    :return: the logger, if found, or a new one with that name
    :rtype: logging.Logger
    """

    logger = logging.getLogger(name)
    level = logging.INFO

    custom_level = user_requested_custom_logging_level()
    if custom_level:
        level = custom_level

    logger.setLevel(level)

    formatter = CustomFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
