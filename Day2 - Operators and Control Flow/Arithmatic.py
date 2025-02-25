num1 = int(10) #number 10 will be stored in the variable as int data type
num2 = int(input('Enter a number - ')) #The numbe input the user will be stored in num2 as int data type

print('num1 is - ', num1, 'and it\'s data type is', type(num1))
print('You have entered - ', int(num2))

sum = num1+num2
deff = num1-num2
mul = num1*num2
div = num1/num2
mod = num1%num2
exp = num1**num2
fd = num1//num2

print('Summation of num1 + num2 is - ', sum)
print('Difference of num1 - num2 is - ', deff)
print('Multiplication of num1 * num2 is - ', mul)
print('Division of num1 / num2 is - ', div)
print('Modulus of num1 % num2 is - ', mod)
print('Exponent of num1 ** num2 is - ', exp)
print('Floor Divison of num1 and num2 is - ', fd)

print(deff>sum)
print(num1==num2)
print(num1>num2)
print(fd<=num1)
print(num1>=num2)
print(exp>1000)
print(num1!=num2)

a, b = (False, True)
print('\n')
print(a)
c = a+1
print(c)
print(b)



