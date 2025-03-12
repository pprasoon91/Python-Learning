file = open('welcome.txt', 'w') #this will create a file welocme.txt if it doesnot exists
file.write('Hello Guys.\nHope you are enjoying learning Python.\n') #this will start writing the file with the given content
file.write('Python makes file handling easy.')
file.close() #this will close the file
print('File written successfully..!!')

