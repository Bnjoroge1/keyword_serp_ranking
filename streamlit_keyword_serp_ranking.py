import streamlit as st
import requests
import os
import pandas as pd

# Function to read keywords from a CSV file
def read_keywords_from_csv(file):
    df = pd.read_csv(file)
    # Assuming the keywords are in the first column
    return df.iloc[:, 0].tolist()

# Streamlit UI components
api_key = os.environ.get('API_KEY')

# Title of the Streamlit app
st.title("Keyword SERP Ranking - Titles & URLs")

# Input fields for user
keywords_input = st.text_input("Please enter the keyword(s) (separated by commas if multiple):")
google_domain = st.text_input("Please enter the Google domain (e.g. 'google.co.uk'):")
gl = st.text_input("Please enter the Google country (e.g. 'uk'):")
hl = st.text_input("Please enter the user UI language (e.g. 'en'):")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file with keywords (one per line):", type=["csv"])

# Determine the source of keywords: CSV or manual input
if uploaded_file is not None:
    keywords = read_keywords_from_csv(uploaded_file)
elif keywords_input:
    keywords = [keyword.strip() for keyword in keywords_input.split(",")]
else:
    keywords = []

# Button to trigger the API call
if st.button('Get Results') and keywords:
    # Initialize the progress bar and status text
    progress_bar = st.progress(0)
    status_text = st.empty()

    combined_csv_data = ""
    for index, q in enumerate(keywords):
        # Update the status text
        status_text.text(f"Fetching data for keyword: {q} ...")

        # Set up the request parameters
        params = {
            'api_key': api_key,
            'q': q,
            'google_domain': google_domain,
            'gl': gl,
            'hl': hl,
            'max_page': '5',
            'num': '100',
            'output': 'csv',
            'csv_fields': 'search.q,organic_results.position,organic_results.title,organic_results.link'
        }

        # Make the HTTP GET request
        api_result = requests.get('https://api.valueserp.com/search', params)
        csv_data = api_result.content.decode("utf-8")
        combined_csv_data += csv_data + "\n"

        # Update the progress bar
        progress_bar.progress((index + 1) / len(keywords))

    # Completion message
    status_text.text("Data fetching complete! You can now download the CSV.")

    # Download button
    st.download_button(
        label="Download CSV",
        data=combined_csv_data,
        file_name="keyword_ranking_results.csv",
        mime="text/csv"
    )
