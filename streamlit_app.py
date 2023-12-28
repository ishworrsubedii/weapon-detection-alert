import os
import requests
import streamlit as st

LOG_DIR = "logs"  # Adjust the log directory as needed

# Update the API URL based on your FastAPI deployment
API_URL = "http://localhost:8000"


def call_api(endpoint):
    try:
        response = requests.post(f"{API_URL}/{endpoint}")
        return response.json()
    except Exception as e:
        return {"error": str(e)}


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


def main_streamlit():
    st.sidebar.header("Weapon Detection and Location Sharing Alert Systems")

    selected_option = st.sidebar.selectbox('Select an option',
                                           ["Start IP Cam Server", "Stop IP Cam Server",
                                            "Start Detection service", "Stop Detection service",
                                            "View Location", "Logs"])

    if selected_option == "Start IP Cam Server":
        if st.button('Start Server'):
            result = call_api("start_ipcam_server")
            st.write(result)

    elif selected_option == "Stop IP Cam Server":
        if st.button('Stop Server'):
            result = call_api("stop_ipcam_server")
            st.write(result)

    elif selected_option == "Start Detection service":
        if st.button('Start Server'):
            result = call_api("start_detection_service")
            st.write(result)

    elif selected_option == "Stop Detection service":
        if st.button('Stop Server'):
            result = call_api("stop_detection_service")
            st.write(result)

    elif selected_option == "View Location":
        view_location()

    elif selected_option == "Logs":
        view_logs()

    else:
        st.write("You selected an option. Add code to handle this option.")


if __name__ == '__main__':
    main_streamlit()
