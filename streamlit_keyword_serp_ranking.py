import streamlit as st
import requests
import os
api_key = os.environ.get('API_KEY')

# Title of the Streamlit app
st.title("Keyword SERP Ranking - Titles & URLs")

# Input fields for user
q = st.text_input("Please enter the keyword:")
google_domain = st.text_input("Please enter the Google domain (e.g. 'google.co.uk'):")
gl = st.text_input("Please enter the Google country (e.g. uk):")
hl = st.text_input("Please enter the user UI language (e.g. en):")

# Button to trigger the API call
if st.button('Get Results'):
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

    # Make the HTTP GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)

    csv_data = api_result.content.decode("utf-8")

    # Providing the CSV content as a downloadable file
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="value_serp_results.csv",
        mime="text/csv"
    )
