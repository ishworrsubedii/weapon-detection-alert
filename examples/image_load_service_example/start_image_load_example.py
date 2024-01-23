import os
import sys
import time
import threading
from services.image_capture_service.image_load_main import ImageLoadThreading

class StartImageLoadServiceExample:
    def __init__(self, flag_path, image_path_img):
        self.flag_path = flag_path
        self.image_load_threading = ImageLoadThreading(image_path_img)
        self.process_queue_thread = threading.Thread(target=self.process_queue)

    def create_start_flag(self):
        try:
            with open(self.flag_path, 'w') as flag_file:
                flag_file.write('False')  # Set initial content as 'False'
        except Exception as e:
            print(f"Error creating start flag file: {e}")

    def read_start_flag(self):
        try:
            with open(self.flag_path, 'r') as flag_file:
                content = flag_file.read().strip().lower()
                return content
        except Exception as e:
            print(f"Error reading start flag: {e}")
            return None

    def update_start_flag(self, value):
        try:
            if os.path.exists(self.flag_path):
                os.remove(self.flag_path)
            with open(self.flag_path, 'w') as flag_file:
                flag_file.write(str(value))
        except Exception as e:
            print(f"Error updating start flag: {e}")

    def start_service(self):
        self.process_queue_thread.start()

        while True:
            flag_value = self.read_start_flag()
            try:
                if flag_value is not None:
                    if flag_value == 'false':
                        self.image_load_threading.start_load_image()
                    elif flag_value == 'true':
                        self.image_load_threading.stop_load_image()
                        break
                    else:
                        print("Stopping the service...")
                        sys.exit()

            except Exception as e:
                print(f"Exception occurred: {e}")
                break

            time.sleep(2)

        self.process_queue_thread.join()

    def process_queue(self):
        while True:
            if not self.image_load_threading.image_queue.empty():
                image_path = self.image_load_threading.image_queue.get()
                self.image_load_threading.process_image(image_path)
            time.sleep(0.5)

if __name__ == '__main__':
    FLAG_PATH = "resources/flag_load_image"
    IMAGE_PATH_IMG = "images/cam_images"

    image_capture_service = StartImageLoadServiceExample(FLAG_PATH, IMAGE_PATH_IMG)
    image_capture_service.create_start_flag()

    image_capture_service.start_service()
