import pandas as pd

dict1 = {
        "Name": ['Ram', 'Shyam', 'Mohan'],
        "Age": [32, 31, 25]
        }

print(type(dict1))
print(dict1)
print(dict1.keys())
print(dict1['Age'])

data = pd.DataFrame(dict1)

print(data)

