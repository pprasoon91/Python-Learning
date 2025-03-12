file = open('welcome.txt', 'r')
content = file.read()
file.close()
print('\n' + content + '\n')


#If you will use "with open()" then file closing is not needed
print('OPENING FILE USING WITH OPEN')
with open('welcome.txt', 'r') as file:
    content = file.read()
print(content)
