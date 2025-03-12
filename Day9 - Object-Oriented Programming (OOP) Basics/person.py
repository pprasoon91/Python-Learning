class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"Name: {self.name}; Age: {self.age}")

person1 = Person('Ram', 32)
person2 = Person('Shyam', 31)
person3 = Person('Mohan', 30)

person1.show()
person2.show()
person3.show()


'''
✔ Defines a Person class with attributes name and age.
✔ Uses __init__() to initialize the attributes properly.
✔ Defines a method show() to display the details of a person.
✔ Creates multiple instances (person1, person2, person3) with different values.
✔ Calls the show() method to print the attributes of each person.
'''