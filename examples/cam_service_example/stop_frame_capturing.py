from services import ipcam_logger

ipcam_logger = ipcam_logger()
STOP_FLAG_PATH = "resources/flag"  # Path to the stop flag file


def write_stop_flag():
    try:
        with open(STOP_FLAG_PATH, 'w') as flag_file:
            flag_file.write("True")
        ipcam_logger.info("Stop flag set.")
    except Exception as e:
        ipcam_logger.error(f"Error setting stop flag: {e}")


if __name__ == "__main__":
    write_stop_flag()
