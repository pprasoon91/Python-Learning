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

# 1. append
l.append('mohan') #this will append mohan as string data type in the end of the list
print(l) #after appending if you will print the list every time it will show you the list with append element in the end of the list

# 2. insert
l.insert(3, 'd') #This will insert d as string data type element at index number 3 in the list l
print(l) #Here you will see the inserted element and the appended element both as it is being printed after append and insert operations
