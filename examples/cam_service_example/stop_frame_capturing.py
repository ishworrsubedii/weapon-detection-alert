import os
from services import ipcam_logger


class StopImageCaptureServiceExample:
    def __init__(self, stop_flag_path):
        self.stop_flag_path = stop_flag_path
        self.logger = ipcam_logger()

    def stop_example_ipcam_webcam(self):
        try:
            with open(self.stop_flag_path, 'w') as flag_file:
                flag_file.write("True")
            self.logger.info("Stop flag set.")
            # os.remove(self.stop_flag_path)
        except Exception as e:
            self.logger.error(f"Error setting stop flag: {e}")


if __name__ == "__main__":
    STOP_FLAG_PATH = "resources/flag"
    stop_load_image_example = StopImageCaptureServiceExample(STOP_FLAG_PATH)
    stop_load_image_example.stop_example_ipcam_webcam()
