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