

'''
******************************************
url = "https://api.github.com"
response = requests.get(url)
print(response.status_code)
******************************************

The above code will give attribute error
why iy is happening:
1. Python first looks for modules in the current directory before searching installed packages.
2. Since script is named requests.py, when you run import requests, Python imports your script instead of the actual requests library.
3. script does not contain a get() function, so Python throws an AttributeError.

FIX:
modify the file name form requests.py to something else.
'''

# Now the same code will not give any error
import requests

url = "https://api.github.com"
response = requests.get(url) # this will return the status code 200. in HTTP status code 200 means sucess It means that your request to "https://api.github.com" was successful, and the server returned the expected response.
print(response.status_code) # this will print the status code 200
#print(response.text) # Prints the response data in JSON format
content = response.text
file = open('test.json', 'w')
file.write(content)
file.close()
with open('test.json', 'r') as file:
    content1 = file.read()
    print(content1)
    print('\n\n')

