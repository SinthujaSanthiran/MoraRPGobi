import streamlit as st
from pathlib import Path
from llama_index import download_loader
from pandasai.llm.openai import OpenAI

# Initialize the AI
llm = OpenAI()
PandasAIReader = download_loader("PandasAIReader")
loader = PandasAIReader(llm=llm)

# Define the path to your CSV file
file_path = Path('./data/your_file_name.csv')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Display the DataFrame
st.write(df)

# Get a question from the user
query = st.text_input("Enter your question")

if query:
    response = loader.run_pandas_ai(df, query, is_conversational_answer=True)
    st.write(response)
