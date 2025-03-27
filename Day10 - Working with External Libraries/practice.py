# Creating a list with a mix of characters, numbers, and names
list1 = ['a', 'b', 'c', 1, 2, 3, 4, 4, 5, 7, 'Ram', 'Shyam', 'Mohan']

# Reversing the order of elements in list1
list1.reverse()

# Printing the reversed list1
print(list1)  

# Creating another list with numbers (including duplicates)
list2 = [1, 4, 6, 4, 7, 2, 4, 1, 23, 12, 11, 15, 99, 88, 76, 65]

# Sorting list2 in **ascending order** (smallest to largest)
list2.sort()

# Printing the sorted list2
print(list2)  

# Reversing list2 to get it in **descending order** (largest to smallest)
list2.reverse()

# Printing the reversed list2
print(list2)  

# Counting how many times **4** appears in list2
print(list2.count(4))  

# Converting list2 into a **set** (removes duplicate values automatically)
set1 = set(list2)  

# Printing the data type of set1 to confirm it's a set
print(type(set1))  # Output: <class 'set'>

# Converting set1 back into a list
list2 = list(set1)  

# Printing the data type of list2 after conversion
print(type(list2))  # Output: <class 'list'>

# Printing the modified list2 (it now contains only unique values)
print(list2)  

# Sorting list2 again in ascending order (to maintain order after removing duplicates)
list2.sort()

# Printing the final sorted list2
print(list2)  



'''

🔹 Summary of What Happens

    list1.reverse() → Flips the order of list1.
    list2.sort() → Sorts list2 in ascending order.
    list2.reverse() → Sorts list2 in descending order.
    list2.count(4) → Counts how many times 4 appears in list2.
    set(list2) → Removes duplicate values and creates a set.
    list(set1) → Converts the set back into a list.
    list2.sort() → Sorts list2 again after duplicates are removed.

'''