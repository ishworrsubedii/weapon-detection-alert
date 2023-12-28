import os
from datetime import datetime
import threading
import cv2 as cv
from PIL import Image
import imagehash
import time
from services import main_sys_logger, ipcam_logger
from utils.settings import get_frame_save_dir


class FrameSaver:
    def __init__(self, source, image_path_to_save, image_hash_threshold):
        self.source = source
        self.image_path_to_save = image_path_to_save or get_frame_save_dir()
        self.thread_running = False
        self.frame_save_thread = None
        self.cap = cv.VideoCapture(self.source)
        self.main_sys_logger = main_sys_logger()
        self.ipcam_logger = ipcam_logger()
        self.image_hash_threshold = image_hash_threshold

    def start_stream(self):
        self.frame_save_thread = threading.Thread(target=self.video_webcam_frame_extraction)
        self.frame_save_thread.start()
        self.thread_running = True

    def stop_stream(self):
        try:
            if self.thread_running:
                self.thread_running = False
                self.frame_save_thread.join()
            self.cap.release()
        except Exception as e:
            self.ipcam_logger.exception(f"Error stopping stream: {e}")

    def hashing_diff(self, prev_frame, current_frame):
        if prev_frame is None:
            return None
        else:
            hash1 = imagehash.average_hash(Image.fromarray(prev_frame))
            hash2 = imagehash.average_hash(Image.fromarray(current_frame))
            return hash2 - hash1

    def save_frame(self, frame):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = os.path.join(self.image_path_to_save, f"{current_time}.jpg")
        success = cv.imwrite(name, frame)
        if success:
            self.ipcam_logger.info(f"Saved {name}...")
        else:
            self.ipcam_logger.error(f"Failed to save image: {name}")

    def video_webcam_frame_extraction(self):
        try:
            previous_frame = None
            while self.cap.isOpened() and self.thread_running:
                success, frame = self.cap.read()
                if success:
                    hash_diff = self.hashing_diff(previous_frame, frame)
                    if hash_diff is None or hash_diff > self.image_hash_threshold:
                        self.save_frame(frame)
                    previous_frame = frame
        except Exception as e:
            self.ipcam_logger.exception(f"Exception occurred: {e}")
            self.stop_stream()


if __name__ == '__main__':
    source = "rtsp://192.168.1.106:8080/h264_opus.sdp"
    image_path_to_save = "images/cam_images"
    start_stop = FrameSaver(source, image_path_to_save, image_hash_threshold=5)

    try:
        start_stop.start_stream()
        time.sleep(1)
    except Exception as e:
        start_stop.ipcam_logger.exception(f"Error starting stream: {e}")

    finally:
        start_stop.stop_stream()
