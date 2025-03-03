sentence = '''Hello everyone....!!
This is a python tutorial.
This is Day 5 of the tutorial.
Hope you are having clear understanding of all the topice covered till date..!!
Happy Learning Python'''

a = sentence.split()
print(type(a))
print(a)
print(len(a))


for i in range(len(a)):
    print(a[i], 'appered', a.count(a[i]), 'time in the sentence..!!')
