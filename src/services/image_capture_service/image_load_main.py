import os
import time
import threading
from src.services.weapon_det_service.weapon_detection_service import DetectionService
import cv2


class ImageLoad:
    def __init__(self, image_dir, model_path, ):
        self.flag = False
        self.thread_running = False
        self.image_load = None
        self.image_path_img = image_dir
        self.latest_image_path = None
        self.detection_service = DetectionService(
            model_path=model_path,
        )
        self.filename = None
        self.display = True

        self.image_info_save = None
        self.original_image = None
        self.bbox = None
        self.image_display_thread = None

    def start_load_image(self):
        """
        Start the image loading thread
        :return:
        """
        self.image_load = threading.Thread(target=self.image_list)

        self.image_load.start()

        self.thread_running = True

    def stop_load_image(self):
        """
        Stop the image loading thread
        :return:
        """
        if self.thread_running:
            self.thread_running = False

            self.image_load.join()
            print("Stopping the image loading thread...")

    def image_list(self):
        """
        This function is used to load the image from the image directory
        :return: None
        """
        time.sleep(0.1)
        while self.thread_running:
            files = sorted(os.listdir(self.image_path_img))
            for self.filename in files:
                if not self.thread_running:
                    break

                image_path = os.path.join(self.image_path_img, self.filename)

                self.latest_image_path = image_path
                print("Processing:", self.latest_image_path)

                rd = cv2.imread(self.latest_image_path)
                time.sleep(0.5)
                if rd is not None:
                    results = self.detection_service.image_det_save(image_path=self.latest_image_path,
                                                                    thresh=0.5,
                                                                    )
                    cv2.waitKey(3)
                    print('done')
                    os.remove(self.latest_image_path)
                else:
                    print('Image Loading Failed .......')


if __name__ == '__main__':
    image_load = ImageLoad(
        image_dir='images/cam_images',
        model_path='resources/models/v1/best.pt',
    )

    image_load.start_load_image()
    # time.sleep(10)
    # image_load.stop_load_image()
    # print("Exiting the program...")
