import requests

url = "https://www.isro.gov.in/robots.txt"

response = requests.get(url)
print(response.status_code)

print(response.text)