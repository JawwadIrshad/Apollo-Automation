import logging
import datetime
import os

def setup_logger():
    """
    Sets up the logger with a filename based on today's date.
    """
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)

    log_filename = os.path.join(log_folder, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    return logger
