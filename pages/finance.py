import streamlit as st
from pathlib import Path
from llama_index import download_loader
from pandasai.llm.openai import OpenAI

# Initialize the AI
llm = OpenAI()
PandasCSVReader = download_loader("PandasCSVReader")
loader = PandasCSVReader(llm=llm)

uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file is not None:
    # Convert the uploaded file to a BytesIO object and read it into a pandas DataFrame
    import io
    import pandas as pd
    df = pd.read_csv(io.BytesIO(uploaded_file.read()))

    # Save the DataFrame to a CSV file
    file_path = './uploaded.csv'
    df.to_csv(file_path, index=False)

    # Use the loader to load the data from the CSV file
    documents = loader.load_data(file=Path(file_path))

    # Display the DataFrame
    st.write(df)

    # Get a question from the user
    query = st.text_input("Enter your question")

    if query:
        response = loader.run_pandas_ai(df, query, is_conversational_answer=False)
        st.write(response)
