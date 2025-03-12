import csv

file = open('student_data.csv', 'w') #csv file object creation
writer = csv.writer(file) #writer object is created
writer.writerow(['Name', 'Age', 'Place'])

writer.writerows([
    ['Ram', '23', 'Delhi'],
    ['Sita', '22', 'Patna'],
    ['Syam', '25', 'Gujrat'],
    ['Gita', '26', 'Punjab']
    ])

file.close()
print('File written Successfully')