name = input('Enter your name - ') # This is an input function which will let user to provide input and store it in the varable 'name'
print('Welcome', name) # This is an output function which will print the 'name' content

#modifying input function to enter 2 entries in one line

num1, num2 = input('Enter two numbers - ').split() #This will split the number and store it in num1 and num2 variable as string data type
a = num1+num2 #here the output of a will be concatenated as the number has been stored as string data type
print('you have entered ', num1, 'and', num2, '\nThe sum of num1 and num2 is - ', a) # if num1 is 23 and num2 24 then output of a will be 2334

num1 = int(num1) #Here num1 is getting converted to int date type, means what ever is stored in previous num1 and num2 variable will be converted into int data type and it will be stored again in num1 and num2
num2 = int(num2) #num2 will be get restored in the num2 variable as int data type

a = num1+num2 #here the out of a will be added as num1 and num2 is of int data type
print('\nsum of num1 and num2 is - ', a)
