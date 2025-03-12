
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

# Child class "Bike" inherits from the parent class "Car"
class Bike(Car):  # This is a child class that inherits attributes and methods from the "Car" class.
    
    # Constructor to initialize the Bike object
    def __init__(self, brand, model, year, price, engine_type):  
        # Calling the parent class (Car) constructor using super()
        super().__init__(brand, model, year, price)  
        
        # New attribute specific to Bike class
        self.engine_type = engine_type  

    # Method to display bike details
    def show_details(self):  
        # Printing the bike details, including inherited attributes and its own attribute
        print(f"Bike name: {self.brand}, Model: {self.model}, Year: {self.year}, Price: ${self.price}, Engine Type: {self.engine_type}")  


# Creating multiple car objects with different values
car1 = Car('Toyota', 'Camry', 2025, 50000)         # Creating an object 'car1' with Toyota details
car2 = Car('Renault', 'Duster', 2025, 49000)       # Creating an object 'car2' with Renault details
car3 = Car('Lamborghini', 'Gallardo', 2025, 1500000) # Creating an object 'car3' with Lamborghini details
bike1 = Bike('Splendor', 'Plus', '2011', 46000, 'Petrol')
bike2 = Bike('Splendor', 'Plus+', '2012', 50000, 'Petrol')
bike3 = Bike('Bajaj', 'Avenger', '2025', 200000, 'Petrol')



# Calling the "ShowAttribute" method to display car details
car1.ShowAttribute()  # Displays details of car1 (Toyota)
car2.ShowAttribute()  # Displays details of car2 (Renault)
car3.ShowAttribute()  # Displays details of car3 (Lamborghini)
bike1.show_details()
bike2.show_details()
bike3.show_details()


