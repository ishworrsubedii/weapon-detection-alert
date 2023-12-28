"""
Created By: ishwor subedi
Date: 2023-12-28
"""

import os
import os
from services import ipcam_logger


class StopImageLoadServiceExample:
    def __init__(self, stop_flag_path):
        self.stop_flag_path = stop_flag_path
        self.logger = ipcam_logger()

    def stop_service(self):
        try:
            with open(self.stop_flag_path, 'w') as flag_file:
                flag_file.write("True")
            self.logger.info("Stop flag set.")
        except Exception as e:
            self.logger.error(f"Error setting stop flag: {e}")


if __name__ == "__main__":
    STOP_FLAG_PATH = "resources/flag_load_image"
    webcam_controller = StopImageLoadServiceExample(STOP_FLAG_PATH)
    webcam_controller.stop_service()
