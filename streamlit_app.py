import streamlit as st


def main():
    st.sidebar.header("Weapon Detection and Location Sharing Alert Systems")

    selected_option = st.sidebar.selectbox('Select an option',
                                           ["Start IP Cam Server", "Start Detection service", "View Location", "Data", "Logs"])

    if selected_option == "Start IP Cam Server":
        if st.button('Start Server'):
            st.write("Server started!")

    elif selected_option == "Start Detection service":
        if st.button("Start Detection server"):
            st.write("Detection server started!")

    elif selected_option == "View Location":
        st.write("Enter location information:")
        location_info = st.text_input("Location:")

        if st.button("View Location"):
            st.write(f"Viewing Location: {location_info}")

    elif selected_option == "Data":
        st.write("You selected 'Data'. Add code to handle this option.")

    elif selected_option == "Logs":
        file_path="logs/gun_det.log"
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                st.write("### File Contents:")
                st.code(file_contents)
        except FileNotFoundError:
            st.error("File not found. Please enter a valid file path.")
        st.write("You selected 'Logs'. Add code to handle this option.")


if __name__ == '__main__':
    main()
