#try, except and finally should be used together.

import pdb
try:
    pdb.set_trace() #this will take you line by line during coad debuging.
    num1 = int(input('Enter first number: '))
    num2 = int(input('Enter second number: '))
    a = num1 / num2
    print('Division of', num1, 'by', num2, 'is--->', a)
    print('\n')

except ValueError:
    print('Only numbers are allowed, please enter a number')
    print('\n')

except ZeroDivisionError:
    print('Division with Zero(0) is not possible, Please enter any natural number')
    print('\n')

#except: #This will catch all the error, be carefull while using except without expression as it it not show error for the issue whcih you do not want to handle with except.
#    pass

finally:
    print('this is finally BLOCK')
    print('\n')