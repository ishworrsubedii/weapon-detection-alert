"""
Created By: ishwor subedi
Date: 2024-04-04
"""
import streamlit as st
from PIL import Image

from demos.single_image_inference import single_image_inference

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

st.set_page_config(layout="wide", page_title="Weapon Detection")

st.write("## Weapon Detection")
st.write(
    "This app uses a custom trained yolov8 model to detect weapons in images. Upload an image to see the detection results."
)
st.sidebar.write("## Browse images:")


def process_image(upload):
    """
    Process the uploaded image and display the original and processed images side by side.
    """
    try:
        image = Image.open(upload)
        col1, col2 = st.columns(2)
        col1.write("Original Uploaded Image")
        col1.image(image)

        processed_image = single_image_inference(image)
        col2.write("Predicted Image")
        col2.image(processed_image)
        st.sidebar.markdown("\n")
    except Exception as e:
        st.error(f"Error processing image: {e}")


def handle_upload():
    """
    Handle the file upload process.
    """
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
        else:
            process_image(upload=uploaded_file)


# Call the upload handler
handle_upload()
