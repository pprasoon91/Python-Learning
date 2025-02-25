a = 4 #nuumber "4" has been stored in a varaible "a"
b = 5 #nuumber "5" has been stored in a varaible "b"
c = 6 #nuumber "6" has been stored in a varaible "c"

d = a+ \
b+ \
c+ 0.5 #this can be written in a single line like "d = a+b+c", here escape sequence has been used. this is actualling suming the values stored in a,b and c then storing it to "d"

print(d) # printing the value stored in variable "d"

#below is the example to get the id of the memory block where the value ha sbeen stored
print (id(a)) # it will print the ID of the memory where 4 has been stored
print (id(b)) # it will print the ID of the memory where 5 has been stored
print (id(c)) # it will print the ID of the memory where 6 has been stored
print (id(d)) # it will print the ID of the memory where result of a+b+c has been stored

print(type(a)) # this will tell what data type is tored in this variavle or this variable is of which data type
print(type(d)) # this will tell what data type is tored in this variavle or this variable is of which data type

#Casting Pythin Variable
x = str(10) #
y = int(10)
z = float(10)

print(x, y, z)

del a # This will delete the variable and its value from the memory, here single variable is getting deleted
del b, c, d # This will delete the variable and its value from the memory, here multiple variable is getting deleted
print(a) #This will give an error "NameError: name 'a' is not defined"
print(b) #This will not even executed as program will terminate at print(a) line with error mentioned above
print(c) #This will not even executed as program will terminate at print(a) line with error mentioned above
print(d) #This will not even executed as program will terminate at print(a) line with error mentioned above