#Here you will come to know about the List in Python and its different method
#NOTE: in list count of it's contents/elements starts from zero

#creating a list
l = ['a', 'b', 'c', 'ram', 'shyam', 1, 2, 3.2] #this is a list
print('\n', type(l)) # it will print the data tye of l as clas list

#accessing or printing the list
print(l) # This will print the entire list which has been defined above in the code

print(l[3]) #this will print list L's content which is at 3rd index i.e ram

print(type(l[5])) #this will print the data type of list L's content which is at 5th index i.e 1

print(len(l)) #This will print lenth of list L, means it will print the count of elements in the list


for i in range(len(l)):
    #print(i)
    print(i, '-', l[i], '-', type(l[i])) # this will print all the index number then the contents/elements in the list l along with it's data type


# LIST METHODS

# 1. APPEND
print('APPEND')
l.append('mohan') #this will append mohan as string data type in the end of the list
print(l) #after appending if you will print the list every time it will show you the list with append element in the end of the list

# 2. INSERT
print('INSERT')
l.insert(3, 'd') #This will insert d as string data type element at index number 3 in the list l
print(l) #Here you will see the inserted element and the appended element both as it is being printed after append and insert operations

# 3. REMOVE
print('REMOVE')
l.remove(l[2]) #This will remove the element exists on 2nd index in the list l i.e c. Here element removal has been defined as the element's index position in the list
print(l)
l.remove('shyam') #This will remove shyam from the list. Here element removal has been defined as the element name itself 
l.remove(1) #This will remove element 1 from the list.  Here also element removal has been defined as the element name itself
print(l) #This will print the modified list.

# 4. POP
print('POP')
l.pop(5) #pop only takes integer value and it will just remove the element from the same index number
print(l) # this will print the modified list
l.pop() #if no value is there in the pop() function, in this case it will pop out the last element in the list
print(l) #will print the updated l list

# 5. SORT
print('SORT')
'''
l.sort() #This will not work, as this list contains both sting data types and integer data types
print(l)
'''
m = [1, 4, 9, 100, 50, 95, 0, 2, 5] #new list m is created with integers data type elements
n = ['a', 'z', 'd', 'c', 'b'] ##new list n is created with string data type elements
name = ['ram', 'shyam', 'sita', 'gita', 'abhimanue', 'balram']
fruit = ['apple', 'orange', 'grapes', 'banana']
m.sort() #this will short all integers in assending order
n.sort() #this will short all strings in assending order
name.sort() #this will sort the names in assending order based on it's first letter of each elements
print(m, '\n', n, '\n', name, sep='') #this will print the modified list - m, n and name
print(fruit)

# 6. REVERSE
print("REVERSE")
m.reverse() #this will arrange all the elements of list in reverse order NOTE: reverse does not mean desending order
print(m)
n.reverse() #this will arrange all the elements of list in reverse order NOTE: reverse does not mean desending order
print(n)
name.reverse() #this will arrange all the elements of list in reverse order NOTE: reverse does not mean desending order
print(name)
fruit.reverse() #this will arrange all the elements of list in reverse order NOTE: reverse does not mean desending order
print(fruit)

# 7. INDEX
print('INDEX')
print('index of 50 in list m is: ', m.index(50))
print('index of z in list n is: ', n.index('z'))
print('index of abhimanue in list name is: ', name.index('abhimanue'))
print('index of orange in list fruit is: ', fruit.index('orange'))

# 8. COUNT
print('COUNT')
num = [6, 5, 7, 9, 2, 4, 5, 6, 9, 10, 7, 5, 4, 6, 8, 9, 3, 21, 5, 8, 4, 6, 8] #this is a list containing intigers data types
#print('number 8 has been repeated for', num.count(8), 'number of time')
for i in range(len(num)):
    element = num[i]
    rep = num.count(num[i])
    print(element, 'found for', rep, 'times in the list \"num\"')