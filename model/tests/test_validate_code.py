import unittest
from ..data_preprocessing.validate_code import is_valid_python_code

class TestPythonCodeSyntax(unittest.TestCase):
    def test_valid_code_1(self):
        code = """
def greet(name):
    greeting = f"Hello, {name}!"
    print(greeting)

greet("World")
"""
        self.assertTrue(is_valid_python_code(code))

    def test_valid_code_2(self):
        code = """
for i in range(5):
    print(i)
else:
    print("Done")
"""
        self.assertTrue(is_valid_python_code(code))

    def test_invalid_code_1(self):
        code = """
def add(a, b):
result = a + b
return result

print(add(2, 3))
"""
        self.assertFalse(is_valid_python_code(code))

    def test_valid_code_3(self):
        code = """
while True:
    print("Looping")
"""
        self.assertTrue(is_valid_python_code(code))

    def test_invalid_code_3(self):
        code = """
if True:
print("This should be indented")
"""
        self.assertFalse(is_valid_python_code(code))

    def test_valid_code_4(self):
        code = """
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hi, my name is {self.name} and I am {self.age} years old.")

person = Person("Alice", 30)
person.greet()
"""
        self.assertTrue(is_valid_python_code(code))

    def test_invalid_code_4(self):
        code = """
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hi, my name is {self.name} and I am {self.age} years old.")

person = Person("Alice", 30)
person.greet()
"""
        self.assertTrue(is_valid_python_code(code))

# Run the tests
if __name__ == '__main__':
    unittest.main()
