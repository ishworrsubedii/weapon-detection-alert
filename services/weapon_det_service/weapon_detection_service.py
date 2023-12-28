import cv2 as cv
import os
from yolov7.detector import YoloV7Detector
from services import main_sys_logger, detection_logger


class DetectionService:
    def __init__(self, model_path, cam_image_dir, output_images, use_gpu=True):
        self.model_path = model_path
        self.cam_images_dir = cam_image_dir
        self.output_images_dir = output_images
        self.use_gpu = use_gpu
        self.logger = main_sys_logger()
        self.detection_logger = detection_logger()

    def draw_bounding_boxes(self, bounding_boxes, image):
        try:
            for box in bounding_boxes:
                x1, y1, x2, y2 = map(int, box.bbox)
                cv.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
                self.logger.info(f"Bounding box drawn: {box}")
        except Exception as e:
            self.logger.error(f"Error in draw_bounding_boxes: {e}")
        return image

    def image_det_save(self, image_path, output_path, draw=False, thresh=0.2):
        try:
            image_display = cv.imread(image_path)

            detector = YoloV7Detector(self.model_path)
            bounding_boxes = detector.detect(image_display, thresh=thresh)

            filename = os.path.basename(image_path)
            detection_time = os.path.splitext(filename)[0]
            object_count = sum(1 for box in bounding_boxes if box.confidence > 0)

            detection_info = {
                'image_name': filename,
                'detection_time': detection_time,
                'bounding_boxes': bounding_boxes,
                'detected': object_count > 0
            }

            if draw and object_count > 0:
                bbox_image = self.draw_bounding_boxes(bounding_boxes, image_display)

                output_filename = os.path.splitext(filename)[0] + "_detected.jpg"
                output_full_path = os.path.join(output_path, output_filename)

                cv.imwrite(output_full_path, bbox_image)
                self.logger.info(f"Bounding boxes drawn and saved to {output_full_path}")

            self.logger.info(f"Detection result: {detection_info}")
            self.detection_logger.info(f"Detection result: {detection_info}\n")

            return detection_info
        except Exception as e:
            self.logger.error(f"Error in detect_and_save: {e}")

    def detect_in_webcam(self, draw=False, video_path=0):
        try:
            detector = YoloV7Detector(self.model_path)

            if video_path == 0:
                cap = cv.VideoCapture(0)
                self.logger.info("Webcam detection started.")
            else:
                cap = cv.VideoCapture(video_path)
                self.logger.info("Video detection started.")

            while True:
                ret, frame = cap.read()

                if not ret:
                    self.logger.error('Error retrieving frames from webcam')
                    break

                try:
                    bounding_boxes = detector.detect(frame)
                    detection_info = {
                        'bounding_boxes': bounding_boxes,
                        'detected': len(bounding_boxes) > 0
                    }
                    self.logger.info(f"Results: {detection_info}")
                    self.detection_logger.info(f"Results: {detection_info}")
                except Exception as detect_error:
                    self.logger.error(f"Error in object detection: {detect_error}")
                    break

                if draw and len(bounding_boxes) > 0:
                    frame = self.draw_bounding_boxes(bounding_boxes, frame)

                cv.imshow("video", frame)
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv.destroyAllWindows()
                    break
        except Exception as e:
            self.logger.error(f"Error in detect_in_webcam: {e}")


if __name__ == "__main__":
    detection_service = DetectionService(
        model_path='resources/models/weapon_detector.pt',
        cam_image_dir='images/cam_images',
        output_images='images/detected_image',
        use_gpu=True
    )
    input_image_path = "images/detected_image/img.png"
    output_image_path = os.path.join(detection_service.output_images_dir, os.path.basename(input_image_path))

    detection_service.image_det_save(
        image_path=input_image_path,
        output_path=output_image_path,
        draw=True,
        thresh=0.2
    )
