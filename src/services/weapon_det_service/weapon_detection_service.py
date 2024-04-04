from pathlib import Path
from ultralytics import YOLO


class DetectionService:
    def __init__(self, model_path):
        self.model_path = model_path

    def image_det_save(self, image_path, thresh=0.2):
        """
         This function is used to detect the weapon in the image and save the image with bounding box
        :param image_path: image path to detect the weapon
        :param thresh: threshold value for detection
        :return:
        """

        detector = YOLO(self.model_path)
        results = detector.predict(image_path, conf=thresh, show=False)

        return results


if __name__ == "__main__":
    detection_service = DetectionService(
        model_path='resources/models/v1/best.pt',

    )
    input_image_path = Path(
        "/home/ishwor/Downloads/PY-4856_Crosman-Bushmaster-MPW-Full_1558033480-458822316.jpg")

    detection_service.image_det_save(
        image_path=str(input_image_path),

        thresh=0.2
    )
