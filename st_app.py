import streamlit as st
import requests

def main():
    st.title("Google Cookies Viewer")

    if st.button("Fetch Google Cookies"):
        response = requests.get("http://localhost:8080/make_google_request")
        if response.status_code == 200:
            cookies_str = response.text
            st.markdown("### Cookies from Google:")
            st.text(cookies_str)  # Displaying the cookies string directly
        else:
            st.error("Failed to fetch cookies. Ensure Flask app is running.")
    if st.button("Fetch Google Analytics Data"):
        response = requests.get("http://localhost:8080/make_ganalytics_request")
        if response.status_code == 200:
            html_content = response.text
            st.markdown("### Google Analytics Data:")
            st.write(html_content)
        else:
            st.error("Failed to fetch Google Analytics data. Ensure Flask app is running.")

if __name__ == '__main__':
    main()
