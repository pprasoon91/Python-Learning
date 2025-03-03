
print('USING MATH FUNCTION')
import math

def fact(num):
    return math.factorial(num)

a = int(input('Enter a number to get it\'s factorial: '))
print(fact(a))



#Other method - without using math library
print('USING SELF LOGIC')
def factorial(num):
    mul = 1
    for i in range(num, 0, -1):
        mul = mul*i
    return mul

print(factorial(a))
