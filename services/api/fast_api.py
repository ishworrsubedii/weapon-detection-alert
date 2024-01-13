from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import uvicorn

from examples.cam_service_example.start_frame_capturing import ImageCaptureService
from examples.cam_service_example.stop_frame_capturing import StopImageCaptureServiceExample
from examples.image_load_service_example.start_image_load_example import StartImageLoadServiceExample
from examples.image_load_service_example.stop_image_load_example import StopImageLoadServiceExample

app = FastAPI()


# Helper functions
def start_ipcam():
    flag_path = "resources/flag"
    source = "rtsp://192.168.1.106:3000/h264_opus.sdp"

    image_path_to_save = "images/cam_images"
    image_hash_threshold = 5
    image_capture_start_example = ImageCaptureService(flag_path, source, image_path_to_save,
                                                                  image_hash_threshold)
    image_capture_start_example.start_service()


def stop_ipcam():
    flag_path = "resources/flag"

    image_capture_stop_example = StopImageCaptureServiceExample(flag_path)
    image_capture_stop_example.stop_load_image_example()


def start_detection():
    flag_path = "resources/flag_load_image"

    image_dir_path = "images/cam_images"

    start_load_image_example = StartImageLoadServiceExample(flag_path, image_dir_path)
    start_load_image_example.start_service()


def stop_detection():
    flag_path = "resources/flag_load_image"

    stop_load_image_example = StopImageLoadServiceExample(flag_path)
    stop_load_image_example.stop_service()


# FastAPI Endpoints
@app.post("/start_ipcam_server")
def start_ipcam_server_api():
    try:
        start_ipcam()
        return JSONResponse(content={"message": "IP Cam Server started!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop_ipcam_server")
def stop_ipcam_server_api():
    try:
        stop_ipcam()
        return JSONResponse(content={"message": "IP Cam Server stopped!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/start_detection_service")
def start_detection_service_api():
    try:
        start_detection()
        return JSONResponse(content={"message": "Image loading Server started!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop_detection_service")
def stop_detection_service_api():
    try:
        stop_detection()
        return JSONResponse(content={"message": "Image loading Server stopped!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
