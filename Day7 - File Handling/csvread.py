import csv

with open('student_data.csv', 'r') as file: #file object has been created as file
    reader = csv.reader(file) #reader object has been created as reader
    data = list(reader) #content from reader has been stored in data valiable as list

print(type(data)) #Will print the variable type of the list - data
print(data) #will print the data list contents

    
for row in data: #for loop will iterate for number of rows in the list data
    print(row) #this will print all the rows in the list data


#Other method to print/read csv
print('OTHER METHOD TO READ CSV')
with open('student_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)