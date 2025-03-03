#here you will learn about the TUPPLE in python
#NOTE: Tupple is immutable
#Tupple use paranthesis "()"

a = (1, 2, 5, 'a', 'b', 'cat', 1.5, 5.5, 2, 5) #This is a tupple
print(type(a)) #it will print the class type of a i.e class tupple
print(a)
# a.append('piyush') - as tupple is immutable so this will give you attribute error i.e "AttributeError: 'tuple' object has no attribute 'append'""
ind = a.index('cat')
print('index of cat is in list \"a\" is : ', ind)
count = a.count(2)
print('number of occurance for element \"2\" in the list \"a\" is: ', count)
