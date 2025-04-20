from colorlog import ColoredFormatter
import datetime
import logging

# Create a logger with INFO level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Renomear os níveis de log para 4 letras
logging.addLevelName(logging.DEBUG, "DEBG")
logging.addLevelName(logging.INFO, "INFO")
logging.addLevelName(logging.WARNING, "WARN")
logging.addLevelName(logging.ERROR, "ERRO")
logging.addLevelName(logging.CRITICAL, "CRIT")

# Default formatter for the file (without colors)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-4s | %(message)s", datefmt="%d/%m/%Y %H:%M:%S"
)

# Handler for the log file
file_handler = logging.FileHandler("pix_control.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Custom class to format each component with different colors
class CustomColoredFormatter(ColoredFormatter):
    def formatTime(self, record, datefmt=None):
        # Get formatted date and time
        dt = datetime.datetime.fromtimestamp(record.created)
        if datefmt:
            # Check if datefmt contains a space to split
            if " " in datefmt:
                date_str = dt.strftime(datefmt.split()[0])  # Only the date part
                time_str = dt.strftime(datefmt.split()[1])  # Only the time part
                # Soft colors for date (light blue) and time (aqua green)
                return f"\033[38;5;75m{date_str}\033[0m \033[38;5;80m{time_str}\033[0m"
            else:
                # Handle the case when datefmt doesn't have a space
                return f"\033[38;5;75m{dt.strftime(datefmt)}\033[0m"
        else:
            return ColoredFormatter.formatTime(self, record, datefmt)

    def format(self, record):
        # Original format to start with
        log_fmt = "%(asctime)s | %(log_color)s%(levelname)-4s\033[0m | %(message_color)s%(message)s"

        # Define message color based on log level
        message_colors = {
            "DEBG": "38;5;146",  # Soft lavender
            "INFO": "38;5;114",  # Soft green
            "WARN": "38;5;222",  # Soft yellow
            "ERRO": "38;5;174",  # Soft pink
            "CRIT": "38;5;168",  # Soft red
        }

        # Assign appropriate color to the message
        record.message_color = (
            f"\033[{message_colors.get(record.levelname, '38;5;251')}m"
        )

        # Apply format with custom colors
        self._style._fmt = log_fmt

        return super().format(record)


# Soft colors for log levels
level_colors = {
    "DEBG": "cyan",  # Cyan
    "INFO": "light_green",  # Light green
    "WARN": "yellow",  # Yellow
    "ERRO": "light_red",  # Light red
    "CRIT": "bold_red",  # Bold red for critical errors
}

# Create custom formatter
color_formatter = CustomColoredFormatter(
    "%(asctime)s | %(log_color)s%(levelname)-4s\033[0m | %(message_color)s%(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    log_colors=level_colors,
    reset=True,
)

# Handler for terminal (console) with colors
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(color_formatter)
logger.addHandler(console_handler)

# Log functions for easier use
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
debug = logger.debug