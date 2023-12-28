import os
import time
from services.image_capture_ipcam.capture_main import FrameSaver
from services import ipcam_logger, main_sys_logger


class StartImageCaptureServiceExample:
    def __init__(self, flag_path, source, image_path_to_save, image_hash_threshold):
        self.flag_path = flag_path
        self.source = source
        self.image_path_to_save = image_path_to_save
        self.image_hash_threshold = image_hash_threshold
        self.ipcam_logger = ipcam_logger()
        self.main_sys_logger = main_sys_logger()

    def create_stop_flag(self):
        try:
            if not os.path.exists(self.flag_path):
                with open(self.flag_path, 'w') as flag_file:
                    flag_file.write('False')  # Set initial content as 'False'
                self.ipcam_logger.info("Flag file created and set to 'False'.")
            else:
                with open(self.flag_path, 'r+') as flag_file:
                    flag_file.truncate(0)  # Clear the file content
                    flag_file.write('False')  # Write 'False' to the cleared file
                self.ipcam_logger.info("Flag file exists and set to 'False'.")
        except Exception as e:
            self.ipcam_logger.error(f"Error creating flag file: {e}")

    def check_stop_flag(self):
        try:
            if os.path.exists(self.flag_path):
                with open(self.flag_path, 'r') as flag_file:
                    content = flag_file.read().strip()
                    if content.lower() == "true":
                        return True
            else:
                self.create_stop_flag()  # Create the stop flag file if it doesn't exist
                return False
        except Exception as e:
            self.ipcam_logger.error(f"Error checking stop flag: {e}")
            return False

    def update_stop_flag(self, value):
        try:
            with open(self.flag_path, 'w') as flag_file:
                flag_file.write(str(value))  # Write the provided value to the flag file
        except Exception as e:
            self.ipcam_logger.error(f"Error updating stop flag: {e}")

    def start_service(self):
        try:
            self.ipcam_logger.info(
                "*************************Image Capturing service has been started.*************************\n")

            start_capture = FrameSaver(self.source, self.image_path_to_save, self.image_hash_threshold)
            start_capture.start_stream()

            while True:
                time.sleep(10)
                stop_flag = self.check_stop_flag()
                if stop_flag:
                    self.ipcam_logger.info(
                        "*************************Stop flag detected. Stopping all frame capturing services.*************************\n")
                    start_capture.stop_stream()
                    break  # Break out of the loop to stop capturing services

        except Exception as e:
            self.main_sys_logger.exception(f"Error in setting up FrameSaver: {e}\n")
            self.ipcam_logger.exception(f"Error in setting up FrameSaver: {e}\n")
        finally:
            if 'start_capture' in locals():
                start_capture.stop_stream()


if __name__ == "__main__":
    FLAG_PATH = "resources/flag"
    SOURCE = 'rtsp://192.168.1.106:3000/h264_opus.sdp'
    IMAGE_PATH_TO_SAVE = "images/cam_images"
    IMAGE_HASH_THRESHOLD = 5

    image_capture_service = StartImageCaptureServiceExample(FLAG_PATH, SOURCE, IMAGE_PATH_TO_SAVE, IMAGE_HASH_THRESHOLD)
    image_capture_service.start_service()
