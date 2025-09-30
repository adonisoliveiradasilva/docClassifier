import logging


class ColorFormatter(logging.Formatter):
    """
    Classe responsável por formatar as mensagens de log.
    """
    COLORS = {
        "DEBUG": "\033[37m",
        "INFO": "\033[36m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        levelname_colored = f"{color}{record.levelname}{self.RESET}"
        record.levelname = levelname_colored
        return super().format(record)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    formatter = ColorFormatter("%(asctime)s - %(levelname)s - %(message)s",
                               datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
