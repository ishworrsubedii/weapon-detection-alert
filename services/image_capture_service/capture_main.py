"""
Author: ishwor subedi
Date: 2023-12-28
Project Name:gun-detection

"""
import os
from PIL import Image
from datetime import datetime
import threading
import imagehash
import time
import cv2 as cv
from services import main_sys_logger
from services import ipcam_logger
from utils.settings import get_frame_save_dir


class FrameSaver:
    def __init__(self, source, image_path_to_save, image_hash_threshold):
        self.source = source
        self.image_path_to_save = image_path_to_save
        if self.image_path_to_save is None or not os.path.exists(self.image_path_to_save):
            self.image_path_to_save = get_frame_save_dir()
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
        if self.thread_running:
            self.thread_running = False
            self.frame_save_thread.join()
        self.cap.release()

    def hashing_diff(self, prev_frame, current_frame):
        if prev_frame is None:
            return None
        else:
            hash1 = imagehash.average_hash(Image.fromarray(prev_frame))
            hash2 = imagehash.average_hash(Image.fromarray(current_frame))
            return hash2 - hash1

    def video_webcam_frame_extraction(self):

        try:
            previous_frame = None
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if success:
                    hash_diff = self.hashing_diff(previous_frame, frame)
                    if hash_diff is None or hash_diff > self.image_hash_threshold:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        name = os.path.join(self.image_path_to_save, f"{current_time}.jpg")
                        success = cv.imwrite(name, frame)  # Check for success
                        if success:
                            self.ipcam_logger.info(f"Saved {name}...")
                        else:
                            self.ipcam_logger.error(f"Failed to save image: {name}")
                            # Consider retrying image saving or taking corrective actions here
                    previous_frame = frame
        except Exception as e:
            self.ipcam_logger.exception(f"Exception occurred: {e}")
            try:
                self.stop_stream()  # Attempt to stop stream gracefully
            except Exception as e:
                self.ipcam_logger.exception(f"Failed to stop stream: {e}")


if __name__ == '__main__':
    source = 'rtsp://192.168.1.106:3000/h264_opus.sdp'
    image_path_to_save = "images/cam_images"
    image_hash_threshold = 5
    image_capture_service = FrameSaver(source, image_path_to_save, image_hash_threshold)
    image_capture_service.video_webcam_frame_extraction()
