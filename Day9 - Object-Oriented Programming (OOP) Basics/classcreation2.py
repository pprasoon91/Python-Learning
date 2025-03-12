
# Defining a class named "Car"
class Car:
    # Constructor method that runs when a new object is created
    def __init__ (self, brand, model, year, price):  
        # Assigning values (brand, model, year, price) to the object
        self.brand = brand    # Stores the car's brand name
        self.model = model    # Stores the car's model name
        self.year = year      # Stores the car's manufacturing year
        self.price = price    # Stores the car's price

    # A method to display the car details
    def ShowAttribute(self):  #this is a method to display car details in a simple word - Method is a function inside class
        # Printing the car's details in a readable format
        print(f"Car Brand: {self.brand} Model: {self.model} Year: {self.year} Price: ${self.price}")

# Creating multiple car objects with different values
car1 = Car('Toyota', 'Camry', 2025, 50000)         # Creating an object 'car1' with Toyota details
car2 = Car('Renault', 'Duster', 2025, 49000)       # Creating an object 'car2' with Renault details
car3 = Car('Lamborghini', 'Gallardo', 2025, 1500000) # Creating an object 'car3' with Lamborghini details

# Calling the "ShowAttribute" method to display car details
car1.ShowAttribute()  # Displays details of car1 (Toyota)
car2.ShowAttribute()  # Displays details of car2 (Renault)
car3.ShowAttribute()  # Displays details of car3 (Lamborghini)

