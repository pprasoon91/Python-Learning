import requests
from bs4 import BeautifulSoup

url = "https://www.nseindia.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/"
}

response = requests.get(url, headers=headers)
print('\n', response.status_code, '\n')

web_text = BeautifulSoup(response.text, 'html.parser')

#print('\n***\n', web_text, '\n***\n')  

heading = web_text.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])

print("\n")
#print(heading)
print("\n")

for headings in heading:
    print(headings.text.strip())
