import requests #imported requests to fetch webpage content
from bs4 import BeautifulSoup #imported BeautifulSoup for web scraping

url = "https://dailytechdrip.com/" #stored the url in a variable "url"

response = requests.get(url) #fetching the url from using requests

status = response.status_code #storing the web response code in "Status"

print(status) #printing the status code stored in "stsatus" variable
print(response) #printing all data in 'response' variable
print("\n****\n", response.text, "\n*****\n")

soup = BeautifulSoup(response.text, "html.parser") #parsing all web data in 'soup' variable
print('\n')

# Extracting all headings
print("EXTRACTING HEADINGS")
heading = soup.find_all(["h1", "h2", "h3"]) #finding all types of heading in 'soup' variable

print(heading)
print(len(heading))

for headings in heading:
    print(headings.text.strip())


#Extracting all links
print("EXTRACTING ALL LINKS")
links = soup.find_all('a')

print(links)