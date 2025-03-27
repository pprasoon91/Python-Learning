# Importing the 'requests' library to make HTTP requests.
import requests

# Importing 'BeautifulSoup' from the 'bs4' library for parsing HTML.
from bs4 import BeautifulSoup

# Defining a variable 'url' and assigning it the web address of Google.
url = 'https://www.google.com'

# Sending a GET request to the specified URL and storing the response in the 'response' variable.
response = requests.get(url)

# Printing the HTTP status code of the response.
# A status code of 200 means the request was successful.
print(response.status_code)

# Creating a BeautifulSoup object to parse the HTML content of the webpage.
# 'response.text' contains the raw HTML of the page.
# 'html.parser' is the parser used to interpret the HTML structure.
soup = BeautifulSoup(response.text, 'html.parser')

# Printing the parsed HTML content of the webpage.
print(soup)

# Printing a newline for better readability.
print('\n')

# Extracting and printing the text inside the <title> tag of the webpage.
# The <title> tag contains the title of the webpage.
print(soup.title.text)


'''
Explanation:

    The script sends a request to Google's homepage.
    It checks if the request was successful (HTTP status code 200).
    The script then parses the webpage HTML using BeautifulSoup.
    Finally, it extracts and prints the webpage title.
'''