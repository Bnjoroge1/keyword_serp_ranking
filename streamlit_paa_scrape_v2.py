import streamlit as st
import requests
import os
import pandas as pd

api_key = os.environ.get('API_KEY')

# Title of the Streamlit app
st.title("People Also Ask - Titles & URLs")

# Select input method
input_option = st.radio("Choose input method:", ["Manual Keyword Entry", "CSV File Upload"])

# If user selects Manual Keyword Entry
if input_option == "Manual Keyword Entry":
    keywords_input = st.text_input("Please enter the keyword(s) (separated by commas if multiple):")
    keywords = [keyword.strip() for keyword in keywords_input.split(",")] if keywords_input else []

# If user selects CSV File Upload
elif input_option == "CSV File Upload":
    uploaded_file = st.file_uploader("Choose a CSV file containing a keywords column", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'keywords' in df.columns:
            keywords = df['keywords'].tolist()
        else:
            st.error("CSV does not have a 'keywords' column!")
            keywords = []
    else:
        keywords = []

# Input fields for user
#keywords_input = st.text_input("Please enter the keyword(s) (separated by commas if multiple):")
google_domain = st.text_input("Please enter the Google domain (e.g. 'google.co.uk'):")
gl = st.text_input("Please enter the Google country (e.g. 'uk'):")
hl = st.text_input("Please enter the user UI language (e.g. 'en'):")

# Button to trigger the API call
if st.button('Get Results'):
    # Splitting the keywords input by comma
    keywords = [keyword.strip() for keyword in keywords_input.split(",")]

    # Initialize the progress bar and status text
    progress_bar = st.progress(0)
    status_text = st.empty()

    combined_csv_data = ""
    for index, q in enumerate(keywords):
        # Update the status text to inform the user which keyword is being processed
        status_text.text(f"Fetching data for keyword: {q} ...")

        # Set up the request parameters for each keyword
        params = {
            'api_key': api_key,
            'q': q,
            'google_domain': google_domain,
            'gl': gl,
            'hl': hl,
            'max_page': '5',
            'num': '100',
            'output': 'csv',
            'csv_fields': 'search.q,related_questions.question,related_questions.answer,related_questions.source.link'
        }

# Make the HTTP GET request to VALUE SERP
        api_result = requests.get('https://api.valueserp.com/search', params)
        csv_data = api_result.content.decode("utf-8")
        combined_csv_data += csv_data + "\n"  # Add a newline between results of different keywords

        # Update the progress bar
        progress_bar.progress((index + 1) / len(keywords))

    # Inform the user that the process is complete
    status_text.text("Data fetching complete! You can now download the CSV.")

    # Providing the combined CSV content as a downloadable file
    st.download_button(
        label="Download CSV",
        data=combined_csv_data,
        file_name="paa_scraped_data.csv",
        mime="text/csv"
    )