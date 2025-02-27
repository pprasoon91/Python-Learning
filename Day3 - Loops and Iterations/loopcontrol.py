#using pass statement
for i in range(10):
    if i == 6:
        pass
    else:
        print('pass', i)
        
#using break statement
for i in range(10):
    if i==5:
        break
    else:
        print('break', i)


#using continue statement
for i in range(10):
    if i==5:
        continue
    else:
        print('continue', i)