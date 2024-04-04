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
import cv2 as cv
from src.utils.settings import get_frame_save_dir


class FrameSaver:
    def __init__(self, source, image_path_to_save, image_hash_threshold):
        self.source = source
        self.image_path_to_save = image_path_to_save
        if self.image_path_to_save is None or not os.path.exists(self.image_path_to_save):
            self.image_path_to_save = get_frame_save_dir()
        self.thread_running = False
        self.frame_save_thread = None
        self.cap = cv.VideoCapture(self.source)
        self.image_hash_threshold = image_hash_threshold

    def start_stream(self):
        """
        Start the video stream
        :return:
        """
        self.frame_save_thread = threading.Thread(target=self.video_webcam_frame_extraction)
        self.frame_save_thread.start()
        self.thread_running = True

    def stop_stream(self):
        """
        Stop the video stream
        :return:
        """
        if self.thread_running:
            self.thread_running = False
            self.frame_save_thread.join()
        self.cap.release()

    def hashing_diff(self, prev_frame, current_frame):
        """
        This function is used to calculate the hash difference between the previous frame and the current frame
        :param prev_frame: previous frame
        :param current_frame: current frame
        :return:
        """
        if prev_frame is None:
            return None
        else:
            hash1 = imagehash.average_hash(Image.fromarray(prev_frame))
            hash2 = imagehash.average_hash(Image.fromarray(current_frame))
            return hash2 - hash1

    def video_webcam_frame_extraction(self):
        """
        This function is used to extract the frame from the video stream and save the image if the hash difference is greater than the threshold value.
        :return:
        """

        try:

            previous_frame = None
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if success:
                    hash_diff = self.hashing_diff(previous_frame, frame)
                    if hash_diff is None or hash_diff > self.image_hash_threshold:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        name = os.path.join(self.image_path_to_save, f"{current_time}.jpg")
                        success = cv.imwrite(name, frame)
                        if success:
                            print(f"Saved {name}...")
                        else:
                            print(f"Failed to save image: {name}")
                    previous_frame = frame
        except Exception as e:
            print(f"Exception occurred: {e}")
            try:
                self.stop_stream()
            except Exception as e:
                print(f"Failed to stop stream: {e}")


if __name__ == '__main__':
    source = 'rtsp://ishwor:subedi@192.168.1.106:5555/h264_opus.sdp'
    image_path_to_save = "images/cam_images"
    image_hash_threshold = 5
    image_capture_service = FrameSaver(source, image_path_to_save, image_hash_threshold)
    image_capture_service.video_webcam_frame_extraction()
