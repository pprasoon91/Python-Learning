class NewClass:  # This is a class definition
    def __init__(self, attribute1, attribute2):  # Constructor method (__init__) to initialize object attributes
        self.attribute1 = attribute1  # Assigning the first attribute to the instance
        self.attribute2 = attribute2  # Assigning the second attribute to the instance

# Creating an object (instance) of the class NewClass with values "Toyota" and 30000
car = NewClass("Toyota", 30000)

# Accessing and printing the first attribute of the object 'car'
print(car.attribute1)  # Output: Toyota

# Accessing and printing the second attribute of the object 'car'
print(car.attribute2)  # Output: 30000



