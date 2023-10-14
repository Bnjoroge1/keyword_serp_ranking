import requests
import json

# set up the request parameters
params = {
'api_key': '15748FB8AD9046848F869B344ECB1A75',
  'q': 'pizza',
  'output': 'csv',
  'csv_fields': 'search.q,related_questions.question,related_questions.answer,related_questions.source.link'
}

# make the http GET request to VALUE SERP
api_result = requests.get('https://api.valueserp.com/search', params)

# print the CSV response from VALUE SERP
print(api_result.content) 