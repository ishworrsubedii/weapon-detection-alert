"""
Author: ishwor subedi
Date: 2023-12-28

"""
import os
import yaml
from box import ConfigBox  # we can access the value using dot and key name
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from pathlib import Path
from services import main_sys_logger as logger


@ensure_annotations
def read_yaml_file(path_to_yaml_file: Path) -> ConfigBox:
    """

    :param path_to_yaml_file:
    :return:
    """
    try:
        with open(path_to_yaml_file) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file:{path_to_yaml_file} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """

    :param path_to_directories:
    :param verbose:
    :return:
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
