class Person:

    def __init__(self, name, age, contact, salary):
        self.name = name
        self.age = age
        self.contact = contact
        self.salary = salary

    def get_name(self):
        return self.name

    def get_salary(self):
        return self.salary


jon = Person(name="Jon", age=24, contact="Rajshahi", salary=200000)

# print(jon.get_name())
# print(jon.get_salary())

karim = Person(name="Karim", age=30, contact="Dhaka", salary=2000)

print(karim.get_name())
print(karim.get_salary())
print(karim.name)

person ={
    'name': 'Karim',
    'age': 23
}

person['name']
