import ast

def is_valid_python_code(code):
    """
    Checks if the given Python code has valid syntax.

    Parameters:
    code (str): The Python code to check.

    Returns:
    bool: True if the code is valid, False otherwise.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


def validate_code(data: list) -> list:
    """
    Validate the code in the data.

    Args:
    data (list): List of dictionaries containing 'Question', 'Code', and 'Plain_Text' keys.

    Returns:
    list: List of dictionaries with validation results appended.
    """
    for item in data:
        code = item.get('Code', '')
        if is_valid_python_code(code):
            item['Validation'] = 'Code is valid'
        else:
            item['Validation'] = 'Code has syntax errors'
    return data
