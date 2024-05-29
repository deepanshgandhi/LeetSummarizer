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

        print(add(2, 3)
                """
        self.assertFalse(is_valid_python_code(code))

    def test_invalid_code_2(self):
        code = """
        while True
            print("Looping")
                """
        self.assertFalse(is_valid_python_code(code))

    def test_invalid_code_3(self):
        code = """
        if True:
        print("This should be indented")
                """
        self.assertFalse(is_valid_python_code(code))

    def test_valid_code_3(self):
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
        self.assertFalse(is_valid_python_code(code))

class TestRemoveComments(unittest.TestCase):

    def test_no_comments(self):
        code = "print('Hello, world!')\nprint('No comments here')"
        cleaned_code = remove_comments(code)
        self.assertNotIn('#', cleaned_code)

    def test_multiple_comments(self):
        code = """
        # This is a comment
        print('Hello, world!') # This is another comment
        # Another comment line
        print('Goodbye, world!')
        """
        cleaned_code = remove_comments(code)
        self.assertNotIn('#', cleaned_code)

    def test_lines_with_only_comments(self):
        code = """
        # This is a comment
        # Another comment
        print('Hello, world!')
        """
        cleaned_code = remove_comments(code)
        self.assertNotIn('#', cleaned_code)

    def test_mixed_content(self):
        code = """
        # This is a comment
        x = 10 # Initialize x
        print(x) # Print x
        # End of script
        """
        cleaned_code = remove_comments(code)
        self.assertNotIn('#', cleaned_code)

# Run the tests
if __name__ == '__main__':
    unittest.main()
