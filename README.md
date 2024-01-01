# weapon-detection-alert-location-share
This project focuses on enhancing the security of different places, like public areas and banks, by implementing a robust gun detection and location-sharing system. The system is designed to capture images from an IP camera strategically placed within the bank premises. When a captured image contains an identifiable gun, the system takes appropriate actions, such as sending alerts or sharing the location of the detected firearm.


1. **Image Capture:**

    Utilizes an IP camera to continuously capture images in real-time within the camera range.Images are processed and analyzed for potential gun presence.

2. **Gun Detection:**

    Employs advanced computer vision algorithms for accurate gun detection in captured images.
  The system recognizes various types of firearms and distinguishes them from other objects. 
3. Alert Systems:

    When a gun is detected, the system triggers immediate alerts.
Alerts can be configured to notify security personnel, law enforcement, and relevant authorities.
4. Location Sharing:

    If a gun is detected, the system captures the location of the incident.
The location information is shared in real-time with designated security personnel and law enforcement agencies.
## File Structure
File structure of the project

```commandline

├── config
│   ├── config.ini
│   └── config.yaml
├── examples
│   ├── start_cap.py
│   └── stop_cap.py
├── images
│   ├── cam_images
│   └── detected_image
│       ├── img_1.png
│       └── img.png
├── logs
│   └── gun_det.log
├── resources
│   └── models
│       └── yolov7.pt
├── services
│   ├── entity
│   │   └── __init__.py
│   ├── gun_det_service
│   │   ├── detection_example_cam.py
│   │   └── __init__.py
│   ├── image_capture
│   │   ├── capture_main.py
│   │   ├── __init__.py
│   │   ├── main_start_stop.py
│   │   └── yolov7_detection_example.py
│   ├── image_load
│   │   ├── __init__.py
│   │   ├── main_load.py
│   │   ├── main_start_stop.py
│   │   ├── start_load.py
│   │   └── stop_load.py
│   ├── __init__.py
│   └── location_share
│       └── __init__.py
├── utils
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── settings.cpython-310.pyc
│   └── settings.py
├── Dockerfiles
├── main.py
├── README.md
├── requirements.txt
└── visualization


```




## How to Run

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ishworrsubedii/gun-detection-alert-location-share.git
    cd cd gun-detection
    ```

2. **Create and activate the Conda environment:**
    ```bash
    conda create -n weapon-detection python=3.10 -y
    conda activate gun-detection
    ```

3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Perform Inference/Prediction:**
    ```bash
    python3 main.py
    streamlit run streamlit_app.py
    ```
   
   - We have to run both programs for inference. py for fastapi post request and streamlit for UI for the prediction.


### Docker
```commandline
```
# Future Work

# Recommendations
Your recommendations are highly valuable, and I highly value your insights and suggestions to enhance this project! Feel free to propose new features, report bugs, or suggest improvements.