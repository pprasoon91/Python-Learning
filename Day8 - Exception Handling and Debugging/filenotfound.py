#try:
with open('test.txt', 'r') as file:
    content = file.read()
    print(content)

'''
except FileNotFoundError:
    print('No such file or directory')

finally:
    print('This is finally block')
'''