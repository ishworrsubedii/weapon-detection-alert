"""
Author: ishwor subedi
Date: 2023-12-27

"""
import os

from services import main_sys_logger
import cv2 as cv

main_sys_logger = main_sys_logger()


def get_frame_save_dir():
    """
    Create a directory for saving images from a video.

    :return:
    str: The path of the created or existing directory.
    """
    root_dir = 'images/cam_images'

    frame_dir = os.path.join(root_dir)
    if not os.path.exists(frame_dir):
        main_sys_logger.info(f"<<<<<<<<<<<<<<<<<< Folder created {frame_dir} >>>>>>>>>>>>>>>>>>>>")
        os.makedirs(frame_dir)
    return frame_dir


def imutil(image_path, output_path, new_size=None):
    """
    Resize an image using OpenCV.

    :param image_path: str, path to the input image file.
    :param output_path: str, path to save the resized image.
    :param new_size: tuple, (width, height) of the desired size.
    """
    try:
        image = cv.imread(image_path)

        if new_size is not None:
            image = cv.resize(image, new_size)

        cv.imwrite(output_path, image)
        main_sys_logger.info(f"Image saved to: {output_path}")
    except Exception as e:
        main_sys_logger.error(f"Error in imutil: {e}")


# Example usage:
if __name__ == "__main__":
    # Get the directory for saving frames
    frame_dir = get_frame_save_dir()

    # Example image path and output path
    input_image_path = 'path/to/your/input/image.jpg'
    output_image_path = os.path.join(frame_dir, 'resized_image.jpg')

    # Resize the image and save it
    imutil(input_image_path, output_image_path, new_size=(800, 600))
