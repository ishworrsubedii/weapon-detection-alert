import time
import os
import threading
from services.weapon_det_service.weapon_detection_service import DetectionService
from services import detection_logger

detection_logger = detection_logger()


class ImageLoadThreading:
    def __init__(self, image_path_img):
        self.thread_running = False
        self.image_path_img = image_path_img
        self.latest_image_path = ""
        self.detection_service = DetectionService(
            model_path='resources/models/weapon_detector.pt',
            cam_image_dir='images/cam_images',
            output_images="images/detected_image",
            use_gpu=True
        )
        self.output_image_save_dir = "images/detected_image"

    def start_load_image(self):
        self.thread_running = True
        self.image_load = threading.Thread(target=self.image_list)
        self.image_load.start()

    def stop_load_image(self):
        if self.thread_running:
            print("Stopping the image loading thread...")
            self.thread_running = False
            self.image_load.join()
            print("Image loading thread stopped.")

    def process_image(self, image_path):
        try:

            detection_info = self.detection_service.image_det_save(output_path=self.output_image_save_dir,
                                                                   image_path=self.latest_image_path,
                                                                   draw=True,thresh=0.5)
            os.remove(image_path)

            if detection_info['detected'] is False:
                os.remove(image_path)

            else:
                detection_logger.info(detection_info)
        except Exception as e:
            detection_logger.error(f"Error processing image {image_path}: {str(e)}")  # Log detection error

    def image_list(self):
        time.sleep(10)  # Initial delay before processing
        while self.thread_running:
            files = sorted(os.listdir(self.image_path_img))
            for filename in files:
                image_path = os.path.join(self.image_path_img, filename)
                self.latest_image_path = image_path
                time.sleep(0.5)
                if self.latest_image_path is not None:
                    self.process_image(self.latest_image_path)
                else:
                    pass


if __name__ == '__main__':
    image_path_img = "images/cam_images"
    image_thread = ImageLoadThreading(image_path_img)
    image_thread.start_load_image()
