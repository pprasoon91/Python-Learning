with open('welcome.txt', 'r') as file:
    content = file.read()

data = content.split()
print(data)
sentence = ' '.join(data)
print(sentence)
data.reverse() #this is modifying the old list at the same memory
print(data)
sentence = ' '.join(data) # this - ' ' will join the words/strings in the list data with a space.
print(sentence)