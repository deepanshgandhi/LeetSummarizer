import unittest
from ..data_preprocessing.handle_comments import remove_comments

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