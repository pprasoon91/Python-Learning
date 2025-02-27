
#printing number in range
for i in range(5): #This will print the value from 0 to 4
    print(i)

#printing number in reverse within the range
for i in range(5, 2, -1): # syntax is for(start, stop, step)here start number is 5 and stop number is 2 which is less then 5, by default the for loop starts incrementing the value, means it will go in this way 5, 6, 7. but 2 will never come so this loop will not get executed untill you are change the default counter in reverse and henc -1 has been defined manually in the last so the it will start counting like 5, 4, 3.
    print(i)

#Printing each character in the string
for char in "HELLO": #here char is a variable will fetch each letter from the given string HELLO in every iteration
    print(char)

#cheking the character if it is available in variable as string
story = '''once upon a time
There was a king and a quien
both of thenm died and the story is over'''

for text in story:
    word = input('Enter any string to search if it is in the story - ')
    if word in story:
        print(word, 'is in the story')
    elif word == '0':
        print('This is the story: \n',story)
        print('\nYou EXIT the program successfuly\n')
        break  
    else:
        print(word, 'is NOT in the story')


#nested for loop
for i in range(1):
    for j in range(2):
        for k in range(3):
            print(i , j, k)

