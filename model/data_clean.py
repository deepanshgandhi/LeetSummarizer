import unittest
import pandas as pd

def read_and_validate_excel(file_path: str):
    """
    Read a excel file and validate that it contains only the required columns:
    'Question', 'Code', and 'Plain Text'.

    Parameters:
    file_path (str): The path to the excel file.

    Returns:
    pd.DataFrame: The DataFrame if validation is successful.

    Raises:
    ValueError: If the required columns are not present or if there are extra columns in the excel file.
    """
    # Read the CSV file
    df = pd.read_excel(file_path)
    
    # Define the required columns
    required_columns = ['Question', 'Code', 'Plain Text']
    
    # Check if all required columns are present in the DataFrame
    if not all(column in df.columns for column in required_columns):
        missing_columns = [column for column in required_columns if column not in df.columns]
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for extra columns
    extra_columns = [column for column in df.columns if column not in required_columns]
    if extra_columns:
        raise ValueError(f"Extra columns present: {', '.join(extra_columns)}")
    
    return df

def remove_comments(code: str) -> str:
    """
    Remove comments from the provided Python code.

    Parameters:
    code (str): The input Python code as a string.

    Returns:
    str: The Python code with comments removed.
    """
    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        # Find the position of the comment symbol
        comment_pos = line.find('#')
        if comment_pos != -1:
            # Keep everything before the comment symbol, preserve leading spaces
            cleaned_line = line[:comment_pos].rstrip()
            if cleaned_line:  # Add non-empty lines only
                cleaned_lines.append(cleaned_line)
        else:
            # No comment on this line, keep it as is
            if line.strip():  # Add non-empty lines only
                cleaned_lines.append(line)
    # Join the cleaned lines back into a single string
    cleaned_code = '\n'.join(cleaned_lines)
    return cleaned_code

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

if __name__ == '__main__':
    unittest.main()
