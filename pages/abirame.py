import os
import time
import streamlit as st
import requests
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


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



if st.button("create Index "):
    documents = SimpleDirectoryReader('data').load_data()
    index = GPTSimpleVectorIndex.from_documents(documents)
    index.save_to_disk('index.json')
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    st.info("Index created")



if st.button("Show metrics"):

    response = index.query("based on the popular times what is the expected user count during the spring season")
    st.write(response.response)
