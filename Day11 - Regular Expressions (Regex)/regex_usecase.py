#SEARCHING A PATTERN IN A STRING OR SENTENCE

print('using \"re.search\"')

import re #Importing re module

a = 'the cost is 500 INR' #Storing a string in a variable

pattern = r"\d+" #storing the pattern in the variable

match = re.search(pattern, a) #searching for the pattern in variable 'a' and storing it to 'match'

if match: #if match is found then it will print if match is negative i.e NONE then it will print else statement
    print("Match found: ", match.group(), '\n')
else:
    print("No match found\n")


#SEARCHING ALL PATTERNS IN THE STRING OR SENTENCE
# 're' IS ALREADY IMPORTED HENCE NOT IMPORTING AGAIN

print('using \"re.findall\"')

a1 = 'My Mobile number is 123-456-7898 and 321-654-9876'

pattern1 = r'\d{3}-\d{3}-\d{4}' #this is the pattern diffenation wich will be stored in pattern1 variable

matches = re.findall(pattern1, a1) #this will store the match from patern1 varibal and store in variable 'matches' as list, so here matches will become a list

if matches: #if match is found then it will print if match is negative i.e NONE then it will print else statement
    print("Match Found", matches, '\n')
else:
    print("Match not found\n")