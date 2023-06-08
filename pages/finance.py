from llama_index import download_loader
import os
import time
import streamlit as st
import requests
from llama_index import VectorStoreIndex, SimpleDirectoryReader
import openai

from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine


AsyncWebPageReader = download_loader("AsyncWebPageReader")

loader = AsyncWebPageReader()

links = st.multiselect("select",['https://www.thepythoncode.com/article/extract-google-trends-data-in-python'])

if st.button("load"):
    documents = loader.load_data(urls=links)


index = VectorStoreIndex.from_documents(documents)
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

retriever = VectorIndexRetriever(
    index=index, 
    similarity_top_k=2,
)
# index.save_to_disk('index.json')
# index = VectorStoreIndex.load_from_disk('index.json')
if "index" not in st.session_state:
    st.session_state.index = index
    st.info("Index created")

questi = st.text_input("Enter question")
if st.button("ask bot"):
    reso = st.session_state.index.query(questi)
    st.write(reso)