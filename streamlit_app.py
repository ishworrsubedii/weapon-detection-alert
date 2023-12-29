import os
import requests
import streamlit as st
import pandas as pd
import time

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


def start_ipcam_server():
    global ipcam_server_status
    if not ipcam_server_status:
        result = call_api("start_ipcam_server")
        ipcam_server_status = True
        return result
    else:
        return {"message": "Server is already running."}


def stop_ipcam_server():
    global ipcam_server_status
    if ipcam_server_status:
        result = call_api("stop_ipcam_server")
        ipcam_server_status = False
        return result
    else:
        return {"message": "Server is not running."}


def start_detection_service():
    global detection_service_status
    if not detection_service_status:
        result = call_api("start_detection_service")
        detection_service_status = True
        return result
    else:
        return {"message": "Service is already running."}


def stop_detection_service():
    global detection_service_status
    if detection_service_status:
        result = call_api("stop_detection_service")
        detection_service_status = False
        return result
    else:
        return {"message": "Service is not running."}


def view_location():
    st.write("Enter location information:")
    location_info = st.text_input("Location:")

    if st.button("View Location"):
        st.write(f"Viewing Location: {location_info}")


def view_logs():
    log_files = [file for file in os.listdir(LOG_DIR) if file.endswith(".log")]

    selected_log_file = st.selectbox("Select Log File", log_files)

    file_path = os.path.join(LOG_DIR, selected_log_file)

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            st.write(f"### File Contents: {selected_log_file}")
            st.code(file_contents)
    except FileNotFoundError:
        st.error("File not found. Please select a valid log file.")


def extract_info_from_filename(filename):
    # Example: "2023-12-29 19:59:30.jpg"
    parts = os.path.splitext(filename)[0].split()
    parts2 = parts[0].split('/')
    date = parts2[2]
    time = parts[1]
    image_name = filename

    return date, time, image_name


def create_datatable(image_folder):
    st.subheader("Image DataTable")

    image_files = [file for file in os.listdir(image_folder) if
                   file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    data = {
        "Date": [],
        "Time": [],
        "Image Path": [os.path.join(image_folder, img) for img in image_files]
    }

    for img in image_files:
        date, time, image_name = extract_info_from_filename(img)
        data["Date"].append(date)
        data["Time"].append(time)
        data["Image Name"].append(image_name)

    df = pd.DataFrame(data)
    st.table(df)


def main_streamlit():
    image_folder = "images/cam_images"
    st.sidebar.header("Weapon Detection and Location Sharing Alert Systems")

    container = st.sidebar.empty()

    selected_option = st.sidebar.selectbox('Select an option',
                                           ["IP Cam Service", "Detection Service", "View Location", "Logs"])

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

        # create_datatable(image_folder)

    elif selected_option == "Detection Service":
        st.subheader("Detection Service")
        if st.button('Start Server'):
            result = start_detection_service()
            st.write(result)
        if st.button('Stop Server'):
            result = stop_detection_service()
            st.write(result)

    elif selected_option == "View Location":
        view_location()

    elif selected_option == "Logs":
        view_logs()

    container.subheader("Service Status:")
    container.write(f"IP Cam Service: {'Running' if ipcam_server_status else 'Stopped'}")
    container.write(f"Detection Service: {'Running' if detection_service_status else 'Stopped'}")

    # Delay to update the table and status every second
    time.sleep(1)


if __name__ == '__main__':
    main_streamlit()
