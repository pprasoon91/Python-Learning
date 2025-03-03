#how to create DICTIONARY
#Dictionary is generally defined using  curly braces "{}"

dict1 = {'a', 'b', 'c', 1, 2, 3, 4, 7, 6, 0, 'ram', 'sita', 'gita', 'shyam'} #this is not a dictionary even though the elements are under curly braces. Dictionary should not have only elements, it should have the key as well.
print(type(dict1)) #this will print the class type of "dict" i.e class set

dict2 = {'Name': 'Ram',
         'Age': 42,
         'Role': 'Engineer',
         'Place': 'Bnagalore',
         'Skills': 'c, c++, python, linux, windows'} #This is a Dictionary
print(type(dict2)) #this will give the out for dict2 as clas dict, as this is a proper dictionary

#Printing Dictionary
print('PRINTING DICTIONARY')
print(dict1) #this will print the set
print(dict2) #this will print the dictionary

#Accessing Dictionary Keys and key elements
print('ACCESSING DICTIONARY ELEMENT')
print(dict2['Name']) #this will fetch the elements for key "Name" from dictionary "dict2"
print(dict2['Age'])
print(dict2.keys()) #This will print all the key in one with default format
for i in dict2: #this will also print all the key
    print(i)
print(list(dict2.keys())) #this will also priint keys

#Modefying Values
print('MODIFYING VALUES')
dict2['Age'] = 38 #this will modify the age from 42 to 38
dict2['Level'] = 'L4' #this will append new key with value L4 at the end of the dictionary
print(dict2['Age']) #this will print the modifier age
print(dict2) #this will print the modified dictionary

#Removing Elements
print('REMOVING ELEMENTS')
dict2.pop('Level') #this will remove the newly created key 'Level'
del dict2['Place'] #this will remove the key 'Place'
print(dict2)

#Accessing Values
print('ACCESSING VALUES')
print('values of dict2 are: ', dict2.values()) #this will display all the values of the dictionary
print('this is the complete dictionary dict2: ', dict2)
print('length of dictionary: ', len(dict2)) 

#Accessing Key-Value pair
print('ACCESSING KEY-VALUE PAIR')
print(dict2.items()) #This will return the values in the form of Tupple


