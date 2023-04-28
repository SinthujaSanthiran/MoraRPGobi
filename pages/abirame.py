import os
import time
import streamlit as st
import requests

def save_html_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def list_files_in_folder(folder):
    return os.listdir(folder)

st.title("Google Search Results HTML Downloader")
search_results_url = st.text_input("Enter the search results URL:", "")

if st.button("Download HTML"):
    try:
        response = requests.get(search_results_url)
        if response.status_code == 200:
            if not os.path.exists("data"):
                os.makedirs("data")

            timestamp = int(time.time())
            file_name = f"search_results_{timestamp}.html"
            save_html_to_file(response.text, f"data/{file_name}")
            st.write(f"HTML content saved as '{file_name}' in the 'data' folder.")
        else:
            st.write(f"Error: Failed to fetch the content. Status code: {response.status_code}")
    except Exception as e:
        st.write(f"Error while downloading HTML: {e}")

if os.path.exists("data"):
    st.write("Files available in the 'data' folder:")
    files = list_files_in_folder("data")
    for file in files:
        st.write(file)
else:
    st.write("No 'data' folder found.")
