from llama_index import download_loader
import os
import time
import streamlit as st
import requests
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import openai




AsyncWebPageReader = download_loader("AsyncWebPageReader")

loader = AsyncWebPageReader()
documents = loader.load_data(urls=['https://www.thepythoncode.com/article/extract-google-trends-data-in-python','https://llamahub.ai/'])


index = VectorStoreIndex.from_documents(documents)
# index.save_to_disk('index.json')
# index = VectorStoreIndex.load_from_disk('index.json')
if "index" not in st.session_state:
    st.session_state.index = index
    st.info("Index created")

questi = st.text_input("Enter question")
if st.button("ask bot"):
    reso = st.session_state.index.query(questi)
    st.write(reso)