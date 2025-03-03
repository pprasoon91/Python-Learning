#Set is an unordered collection of unique elements

set1 = {1, 2, 3, 4, 4, 4, 6, 5, 3, 7, 8, 9, 10} #This is a set
print(set1) # it iwll giv the output in sorted form and no duplicate elements will be there

#Set Operations
# 1. Union
print('SET OPERATIONS')
print('1. UNION')
a = {'a', 'b', 'c', 'd', 'e'}
b = {'a', 'e', 'f', 'g', 'h'}
print(a|b)

c = {1, 2, 3, 3, 4, 6, 5}
d = {1, 7, 8, 9, 9, 10, 11}
print(c|d)

# 2. Intersection
print('INTERSECTION')
print(a&b)
print(c&d)
print(b&a)
print(d&c)

# 3. Difference
print('DIFFERENCE')
print(a-b)
print(c-d)
print(b-a)
print(d-c)

# 4. Symmetric Difference
print('SYMMETRIC DIFFERENCE')
print(a^b)
print(c^d)