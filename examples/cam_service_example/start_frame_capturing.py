import os
import time
from services.image_capture_service.capture_main import FrameSaver
from services import ipcam_logger, main_sys_logger

IPCAM_LOGGER = ipcam_logger()
MAIN_SYS_LOGGER = main_sys_logger()


class ImageCaptureService:
    def __init__(self, flag_path, source, image_path_to_save, image_hash_threshold):
        self.flag_path = flag_path
        self.source = source
        self.image_path_to_save = image_path_to_save
        self.image_hash_threshold = image_hash_threshold
        self.running = False

    def create_stop_flag(self):
        try:
            with open(self.flag_path, 'w') as flag_file:
                flag_file.write('False')  # Set initial content as 'False'
            IPCAM_LOGGER.info("Flag file created and set to 'False'.")
        except Exception as e:
            IPCAM_LOGGER.error(f"Error creating flag file: {e}")

    def check_stop_flag(self):
        try:
            if os.path.exists(self.flag_path):
                with open(self.flag_path, 'r') as flag_file:
                    content = flag_file.read().strip()
                    return content.lower() == "true"
            else:
                return False
        except Exception as e:
            IPCAM_LOGGER.error(f"Error checking stop flag: {e}")
            return False

    def update_stop_flag(self, value):
        try:
            with open(self.flag_path, 'w') as flag_file:
                flag_file.write(str(value))  # Write the provided value to the flag file
        except Exception as e:
            IPCAM_LOGGER.error(f"Error updating stop flag: {e}")

    def start_service(self):
        try:
            IPCAM_LOGGER.info("Image Capturing service starting.")
            self.running = True
            start_capture = FrameSaver(self.source, self.image_path_to_save, self.image_hash_threshold)
            start_capture.start_stream()

            while self.running:
                time.sleep(1)
                stop_flag = self.check_stop_flag()
                IPCAM_LOGGER.debug(f"Stop flag status: {stop_flag}")

                if stop_flag:
                    IPCAM_LOGGER.info("Stop flag detected. Stopping all frame capturing services.")
                    self.running = False
                    stop_successful = start_capture.stop_stream()
                    if stop_successful:
                        IPCAM_LOGGER.info("Frame capturing services successfully stopped.")
                    else:
                        IPCAM_LOGGER.warning("Issue encountered while stopping frame capturing services.")

        except Exception as e:
            MAIN_SYS_LOGGER.exception(f"Error in setting up FrameSaver: {e}")
            IPCAM_LOGGER.exception(f"Error in setting up FrameSaver: {e}")
        finally:
            if 'start_capture' in locals():
                stop_successful = start_capture.stop_stream()
                if stop_successful:
                    IPCAM_LOGGER.info("Frame capturing services successfully stopped in finally block.")
                else:
                    IPCAM_LOGGER.warning("Issue encountered while stopping frame capturing services in finally block.")

    def stop_service(self):
        self.update_stop_flag("True")


if __name__ == "__main__":
    FLAG_PATH = "resources/flag"
    SOURCE = 'rtsp://192.168.18.10:3000/h264_opus.sdp'
    IMAGE_PATH_TO_SAVE = "images/cam_images"
    IMAGE_HASH_THRESHOLD = 5

    image_capture_service = ImageCaptureService(FLAG_PATH, SOURCE, IMAGE_PATH_TO_SAVE, IMAGE_HASH_THRESHOLD)
    image_capture_service.create_stop_flag()
    image_capture_service.start_service()
    time.sleep(1)