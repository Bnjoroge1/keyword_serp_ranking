import streamlit as st
import requests
import os
import pandas as pd

# Function to read keywords from a CSV file
def read_keywords_from_csv(file):
    df = pd.read_csv(file)
    return df.iloc[:, 0].tolist()

# Streamlit UI components
api_key = os.environ.get('API_KEY')
st.title("Keyword SERP Ranking - Titles & URLs")

# Radio button for input method
input_method = st.radio("Choose your input method:", ('Manual Input', 'CSV Upload'))

# Conditional input fields based on chosen input method
if input_method == 'Manual Input':
    keywords_input = st.text_input("Please enter the keyword(s) (separated by commas if multiple):")
elif input_method == 'CSV Upload':
    uploaded_file = st.file_uploader("Upload a CSV file with keywords (one per line):", type=["csv"])

google_domain = st.text_input("Please enter the Google domain (e.g. 'google.co.uk'):")
gl = st.text_input("Please enter the Google country (e.g. 'uk'):")
hl = st.text_input("Please enter the user UI language (e.g. 'en'):")

# Determine the source of keywords
if input_method == 'Manual Input' and keywords_input:
    keywords = [keyword.strip() for keyword in keywords_input.split(",")]
elif input_method == 'CSV Upload' and uploaded_file is not None:
    keywords = read_keywords_from_csv(uploaded_file)
else:
    keywords = []

# Button to trigger the API call
if st.button('Get Results') and keywords:
    # Initialize the progress bar and status text
    progress_bar = st.progress(0)
    status_text = st.empty()

    combined_csv_data = ""
    for index, q in enumerate(keywords):
        status_text.text(f"Fetching data for keyword: {q} ...")
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

        api_result = requests.get('https://api.valueserp.com/search', params)
        csv_data = api_result.content.decode("utf-8")
        combined_csv_data += csv_data + "\n"
        progress_bar.progress((index + 1) / len(keywords))

    status_text.text("Data fetching complete! You can now download the CSV.")
    st.download_button(
        label="Download CSV",
        data=combined_csv_data,
        file_name="keyword_ranking_results.csv",
        mime="text/csv"
    )
