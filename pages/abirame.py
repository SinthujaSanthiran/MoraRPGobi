import os
import json
import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def google_search(query):
    search_results = []
    for url in search(query, num_results=20):
        search_results.append(url)
    return search_results

def extract_business_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    business_name = soup.find("h1", class_="section-hero-header-title-title").get_text(strip=True) if soup.find("h1", class_="section-hero-header-title-title") else None
    business_rating = soup.find("span", class_="section-star-display").get_text(strip=True) if soup.find("span", class_="section-star-display") else None
    business_reviews = soup.find("button", class_="section-reviewchart-numreviews").get_text(strip=True) if soup.find("button", class_="section-reviewchart-numreviews") else None

    return {
        "name": business_name,
        "rating": business_rating,
        "reviews": business_reviews,
    }

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

st.title("Google Business Page Scraper")
keyword = st.text_input("Enter a keyword:", "")

if st.button("Search and Save"):
    st.write("Searching for businesses related to:", keyword)
    search_query = f"{keyword} site:google.com/maps"

    results = google_search(search_query)
    business_data = []

    for result in results:
        try:
            data = extract_business_data(result)
            if data["name"]:
                business_data.append(data)
        except Exception as e:
            st.write(f"Error while processing {result}: {e}")

    if business_data:
        if not os.path.exists("data"):
            os.makedirs("data")
        save_to_file(business_data, f"data/{keyword}_business_data.json")
        st.write("Data saved in 'data' folder.")
    else:
        st.write("No businesses found.")
