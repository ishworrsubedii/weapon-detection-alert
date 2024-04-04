"""
Created By: ishwor subedi
Date: 2024-04-04
"""
import cv2 as cv

from src.services.weapon_det_service.weapon_detection_service import DetectionService


def single_image_inference(image_path):
    """
    This function is used to detect the weapon in the image and save the image with bounding box
    :param image_path:  image path to detect the weapon
    :return: image vector with bounding box
    """
    detection_service = DetectionService(
        model_path='resources/models/v1/best.pt',

    )
    results = detection_service.image_det_save(
        image_path=image_path,
        thresh=0.2
    )
    for result in results:
        original_image = result.orig_img
        bbox = result.boxes.xyxy.int().tolist()
        for i, bbox in enumerate(bbox):
            x1, y1, x2, y2 = bbox

            cv.putText(original_image, f'{result.names[result.boxes.cls[i].int().tolist()]}', (x1, y1 - 10),
                       cv.FONT_HERSHEY_SIMPLEX,
                       0.9,
                       (0, 0, 255), 2)
            cv.rectangle(original_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return original_image


if __name__ == '__main__':
    image_path = '/home/ishwor/Desktop/gun-detection/images/cam_images/th-3711382641.jpg'
    image = single_image_inference(image_path)
    cv.imshow('Weapon Detection', image)
    cv.waitKey(0)
    cv.destroyAllWindows()
