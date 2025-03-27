import requests
from bs4 import BeautifulSoup

url = "https://www.indiatoday.in/"

response = requests.get(url)
print('\n', response.status_code, '\n')

web_text = BeautifulSoup(response.text, 'html.parser')

#print('\n***\n', web_text, '\n***\n')

heading = web_text.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])

print("\n")
print(heading)
print("\n")

for headings in heading:
    print(headings.text.strip())
