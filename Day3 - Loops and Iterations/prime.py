#printing prime numbers from between 1 to 100

num = int(input('Enter a number to check PRIME NUMBERS within it: '))
print('\nbelow are the PRIME NUMBERS lies between 0 to ', num, '\n')

for n in range (2, num+1):
    is_prime = True
    for i in range (2, int(n ** 0.5) + 1):
        if n % i == 0:
            is_prime = False
            break

    a = 1
    if is_prime:
        print(a, '-', n, end=" ")
        a = a+1
print('\n')