import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# List of initial keywords
initial_keywords = ['Kite surfing Galle', 'Scuba diving Galle']

# Create a sidebar for keyword selection
selected_keywords = st.multiselect('Select existing keywords', initial_keywords)

# Allow additional keywords to be added
additional_keyword = st.text_input("Add a new keyword")
if additional_keyword:
    selected_keywords.append(additional_keyword)

# When keywords are selected, fetch data from Google Trends and display it
if st.multiselect('Fetch Google Trends data for selected keywords',selected_keywords):
    # Define the payload
    kw_list = selected_keywords

    # Get Google Trends data
    pytrends.build_payload(kw_list, timeframe='all')

    # Get interest over time
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'],axis='columns')

        st.write(data)
    else:
        st.write('The selected keywords do not have enough data to display a trend.')
