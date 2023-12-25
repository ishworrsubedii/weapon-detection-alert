import os
import sys
import logging


def main_sys_logger(log_dir="logs"):
    logging_str = "[%(asctime)s:%(levelname)s:%(module)s:%(message)s]"

    log_path = os.path.join(log_dir, "gun_det.log")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,

        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("main_sys_logger")  # Changed logger name

    return logger


def ipcam_logger(log_dir="logs"):
    logging_str = "[%(asctime)s:%(levelname)s:%(module)s:%(message)s]"

    log_path = os.path.join(log_dir, "ipcam.log")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,

        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("ipcam_logger")  # Changed logger name

    return logger
