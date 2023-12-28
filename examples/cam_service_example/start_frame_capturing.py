import os
import time
from services.image_capture_ipcam.capture_main import FrameSaver
from services import ipcam_logger, main_sys_logger

FLAG_PATH = "resources/flag"

ipcam_logger = ipcam_logger()
main_sys_logger = main_sys_logger()




def create_stop_flag():
    try:
        if not os.path.exists(FLAG_PATH):
            with open(FLAG_PATH, 'w') as flag_file:
                flag_file.write('False')  # Set initial content as 'False'
            ipcam_logger.info("Flag file created and set to 'False'.")
        else:
            with open(FLAG_PATH, 'r+') as flag_file:
                flag_file.truncate(0)  # Clear the file content
                flag_file.write('False')  # Write 'False' to the cleared file
            ipcam_logger.info("Flag file exists and set to 'False'.")
    except Exception as e:
        ipcam_logger.error(f"Error creating flag file: {e}")


def check_stop_flag():
    try:
        if os.path.exists(FLAG_PATH):
            with open(FLAG_PATH, 'r') as flag_file:
                content = flag_file.read().strip()
                if content.lower() == "true":
                    return True
        else:
            create_stop_flag()  # Create the stop flag file if it doesn't exist
            return False
    except Exception as e:
        ipcam_logger.error(f"Error checking stop flag: {e}")
        return False


def update_stop_flag(value):
    try:
        with open(FLAG_PATH, 'w') as flag_file:
            flag_file.write(str(value))  # Write the provided value to the flag file
    except Exception as e:
        ipcam_logger.error(f"Error updating stop flag: {e}")


if __name__ == "__main__":
    source = 'rtsp://192.168.1.106:3000/h264_opus.sdp'  # 0 for webcam, paste your ipcam link to extract from ipcam
    image_path_to_save = "images/cam_images"
    image_hash_threshold = 5

    try:
        ipcam_logger.info(
            "*************************Image Capturing service has been started.*************************\n")

        start_capture = FrameSaver(source, image_path_to_save, image_hash_threshold)
        start_capture.start_stream()

        while True:
            time.sleep(10)
            stop_flag = check_stop_flag()
            if stop_flag:
                ipcam_logger.info(
                    "*************************Stop flag detected. Stopping all frame capturing services.*************************\n")
                start_capture.stop_stream()
                break  # Break out of the loop to stop capturing services

    except Exception as e:
        main_sys_logger.exception(f"Error in setting up FrameSaver: {e}\n")
        ipcam_logger.exception(f"Error in setting up FrameSaver: {e}\n")
    finally:
        if 'start_capture' in locals():
            start_capture.stop_stream()
