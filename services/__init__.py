import os
import sys
import logging


def configure_logger(logger_name, log_filename, log_dir="logs"):
    """
    Configures a logger with specified parameters.

    :param logger_name: Name of the logger.
    :param log_filename: Name of the log file.
    :param log_dir: Directory where logs will be stored. Defaults to "logs".
    :return: Configured logger.
    """
    logging_str = "[%(asctime)s:%(levelname)s:%(module)s:%(message)s]"

    log_path = os.path.join(log_dir, log_filename)
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=logging_str,

        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(logger_name)

    return logger


def main_sys_logger(log_dir="logs"):
    """
    Configures and returns the main system logger.

    :param log_dir: Directory where logs will be stored. Defaults to "logs".
    :return: Main system logger.
    """
    return configure_logger("main_sys_logger", "gun_det.log", log_dir)


def ipcam_logger(log_dir="logs"):
    """
    Configures and returns the IP camera logger.

    :param log_dir: Directory where logs will be stored. Defaults to "logs".
    :return: IP camera logger.
    """
    return configure_logger("ipcam_logger", "ipcam.log", log_dir)


def detection_logger(log_dir="logs"):
    """
    Configures and returns the detection logger.

    :param log_dir: Directory where logs will be stored. Defaults to "logs".
    :return: Detection logger.
    """
    return configure_logger("detection_logger", "detection.log", log_dir)
