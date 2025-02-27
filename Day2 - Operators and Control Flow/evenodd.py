print('\nthis is program to check if the entered number is EVEN or ODD\n')
num = int(input('Enter a number to check if it is EVEN or ODD - '))

a = num%2

if a==0:
    print('\n', num, 'is an EVEN number\n')
#elif (a<=1 and a!=0) or a==2:
#   print('\n', num, 'is PRIME number\n')
else:
    print('\n', num, 'is ODD number\n')