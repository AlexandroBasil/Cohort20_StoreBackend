class Student:

    def __init__(self, name, age=None):
        self.name = name
        self.age = age

    def say_hello(self):
        print("Hello! My name is " + self.name)

print("********** Test 2 *************")

student1 = Student("Alex Garcia", 27)
student1.say_hello()

student2 = Student("Sergio Inzunza", 35)
student2.say_hello()

print(student1.name)
student1.name = "Name Changed"
print(student1.name)
