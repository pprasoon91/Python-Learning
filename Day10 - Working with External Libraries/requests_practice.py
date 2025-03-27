import requests

url = 'https://www.google.co.in'

content = requests.get(url)

print(content.status_code) #this will print the status code
print('\n')
print(content.text) #this will print the html code from the page