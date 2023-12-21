import cv2 as cv
import os
from services import  logger
from yolov7.detector import YoloV7Detector


class CamDetection:

    def __init__(self, model_path, cam_image_dir, output_images):
        self.model_path = model_path
        self.cam_images_dir = cam_image_dir
        self.output_image = output_images

    def draw_bbox(self, bbox, image):
        """

        :param bbox:
        :param image:
        :return:
        """
        try:
            dh, dw, _ = image.shape
            for box in bbox:
                x, y, w, h = box
                x, y, w, h = int(x), int(y), int(w), int(h)
                cv.rectangle(image, (x, y), (w, h), (0, 0, 255), 1)
        except Exception as e:
            logger.error(f"Error in draw_bbox: {e}")
        return image

    def cam_image_detection(self, image_path, draw=True):
        """

        :param image_path:
        :param draw:
        :return:
        """
        try:
            image_display = cv.imread(image_path)
            yolov7_detector = YoloV7Detector(self.model_path)
            model_prediction, conf, classes = yolov7_detector.detect(image_display)

            filename = os.path.basename(image_path)
            detection_time = os.path.splitext(filename)[0]
            count = sum(1 for i in classes if i == 0)
            if count > 0:
                if draw:
                    bbox_image = self.draw_bbox(model_prediction, image_display)
                    filename = os.path.basename(image_path)
                    filename = os.path.join(self.output_image, filename)
                    cv.imwrite(filename, bbox_image)

                return detection_time, count
        except Exception as e:
            logger.error(f"Error in cam_image_detection: {e}")

    def image_detection(self,input_image_path, draw=True ):
        """

        :param draw:
        :param input_image_path:
        :return:
        """
        try:
            image_display = cv.imread(input_image_path)
            yolov7_detector = YoloV7Detector(self.model_path)
            model_prediction, conf, classes = yolov7_detector.detect(image_display)
            if draw:
                bbox_image = self.draw_bbox(model_prediction, image_display)
                filename = os.path.basename(input_image_path)
                filename = os.path.join(self.output_image, filename)
                cv.imwrite(filename, bbox_image)
        except Exception as e:
            logger.error(f"Error in image_detection: {e}")

    def webcam_detection(self, draw=False, video_path=0):
        """

        :param draw:
        :param video_path:
        :return:
        """
        try:
            yolov7_detector = YoloV7Detector(self.model_path)

            if video_path == 0:
                cap = cv.VideoCapture(0)
            else:
                cap = cv.VideoCapture(video_path)

            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.error('Error retrieving frames from webcam')
                    break
                results, conf, classes = yolov7_detector.detect(frame)
                logger.info(f"Results: {results}, Confidence: {conf}, Classes: {classes}")
                if draw:
                    frame = self.draw_bbox(results, frame)
                cv.imshow("video", frame)
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv.destroyAllWindows()
                    break
        except Exception as e:
            logger.error(f"Error in webcam_detection: {e}")


if __name__ == "__main__":
    # Example usage:
    cam_detection = CamDetection(model_path='resources/models/yolov7.pt', cam_image_dir='your_cam_image_dir', output_images='your_output_images')
    cam_detection.webcam_detection(draw=True, video_path=0)