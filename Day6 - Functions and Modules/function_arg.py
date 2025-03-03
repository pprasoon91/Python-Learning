#Arguments allow us to pass data into a function.

#Single Argument
print('SINGLE ARGUEMENT')
def greet(name): #'name' is the parameter
    print('Hello,', name, '..!!')

greet('Piyush') #'Piyush' has been passed for name parameter

#Multiple Arguement
# 1st Example
print('MULTIPLE ARGUMENT')
def greet(name1, name2):
    print('Hello', name1, 'and', name2, '..!!')

greet('Piyush', 'Prasoon')

# 2nd Example
def mul(num1, num2):
    print('multiplication of number', num1, 'and', num2, 'is', num1*num2)

mul(2, 3)

# 3rd Example - Returning the values to the called function
def sum(num1, num2):
    return num1+num2 #this will return the value to the place where function has been called

addition = sum(4, 5) #returned value from called function has been stroed in the variable 'addition'
print('Result is:', addition) #value stored in addition will be printed here

# 4th Default Arguments
print('DEFAULT ARGUMENT')
def power(base, exponent=2): #here second argument has been predefines for default input 2, but if any parameter will be passed then the exponent will get that value rather getting default value 2
    return base**exponent

pow = power(100, 3)
print('power - ', power(10, 3)) #here second argument is 3 so exponent will get the value 3
print('power - ', power(10)) #here seconf argumrnt is not passed for the exponent will take default value as 2