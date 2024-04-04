import os
import requests
import streamlit as st
import pandas as pd
import uvicorn

from src.api.fast_api import app

LOG_DIR = "logs"
API_URL = "http://localhost:8000"

ipcam_server_status = False
detection_service_status = False


def call_api(endpoint):
    try:
        response = requests.post(f"{API_URL}/{endpoint}")
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def start_stop_server(start_message, already_running_message, not_running_message):
    global ipcam_server_status, detection_service_status
    if not ipcam_server_status:
        result = call_api("start_ipcam_server")
        ipcam_server_status = True
        return {"message": start_message, "result": result}
    else:
        return {"message": already_running_message}


def start_ipcam_server():
    return start_stop_server("IP Cam Server started.", "IP Cam Server is already running.",
                             "IP Cam Server is not running.")["result"]


def stop_ipcam_server():
    global ipcam_server_status
    if ipcam_server_status:
        result = call_api("stop_ipcam_server")
        ipcam_server_status = False
        return {"message": "IP Cam Server stopped.", "result": result}
    else:
        return {"message": "IP Cam Server is not running."}


def start_detection_service():
    return start_stop_server("Detection Service started.", "Detection Service is already running.",
                             "Detection Service is not running.")["result"]


def stop_detection_service():
    global detection_service_status
    if detection_service_status:
        result = call_api("stop_detection_service")
        detection_service_status = False
        return {"message": "Detection Service stopped.", "result": result}
    else:
        return {"message": "Detection Service is not running."}


def extract_info_from_filename(filename):
    parts = os.path.splitext(filename)[0].split()

    date, time = parts[0], parts[1]

    return date, time, filename


def create_datatable(image_folder):
    st.subheader("Image DataTable")

    image_files = [file for file in os.listdir(image_folder) if
                   file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    data = {"Date": [], "Time": [], "ImageName": []}

    for img in image_files:
        date, time, image_name = extract_info_from_filename(img)
        data["Date"].append(date)
        data["Time"].append(time)
        data["ImageName"].append(image_name)

    df = pd.DataFrame(data)

    # Convert Date and Time columns to datetime for sorting
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    # Sort DataFrame by DateTime in descending order
    df = df.sort_values(by='DateTime', ascending=False).drop('DateTime', axis=1)

    st.table(df)


def main_streamlit():
    global ipcam_server_status, detection_service_status

    image_folder = "images/cam_images"
    st.sidebar.header("Weapon Detection and Location Sharing Alert Systems")

    container = st.sidebar.empty()

    selected_option = st.sidebar.selectbox('Select an option',
                                           ["IP Cam Service", "Detection Service"])

    if selected_option == "IP Cam Service":
        st.subheader("IP Cam Service")
        if st.button('Start Server'):
            result = start_ipcam_server()
            st.write(result)
        if st.button('Stop Server'):
            result = stop_ipcam_server()
            st.write(result)
        if st.button('Refresh Datatable'):
            create_datatable(image_folder)

    elif selected_option == "Detection Service":
        st.subheader("Detection Service")
        if st.button('Start Server'):
            result = start_detection_service()
            st.write(result)
        if st.button('Stop Server'):
            result = stop_detection_service()
            st.write(result)

    container.subheader("Service Status:")
    container.write(f"IP Cam Service: {'Running' if ipcam_server_status else 'Stopped'}")
    container.write(f"Detection Service: {'Running' if detection_service_status else 'Stopped'}")


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
    main_streamlit()
