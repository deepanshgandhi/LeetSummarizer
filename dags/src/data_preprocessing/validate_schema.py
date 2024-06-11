def validate_schema(data: list) -> list:
    """
    Validate the schema of the data.

    Args:
    data (list): List of dictionaries containing 'Question', 'Code', and 'Plain_Text' keys.

    Raises:
    ValueError: If the schema validation fails for any item in the data.
    """
    try:
        for idx, item in enumerate(data):
            # Ensure that each dictionary item contains the required keys
            if 'Question' not in item or 'Code' not in item or 'Plain Text' not in item:
                raise ValueError(f"Validation failed for item at index {idx}: Missing required keys.")
            # Check if the Code key is a non-empty string
            if not isinstance(item['Code'], str) or not item['Code'].strip():
                raise ValueError(f"Validation failed for item at index {idx}: Invalid or empty 'Code' value.")
            # Check if the Question key is a non-empty string
            if not isinstance(item['Question'], str) or not item['Question'].strip():
                raise ValueError(f"Validation failed for item at index {idx}: Invalid or empty 'Question' value.")
            # Check if the Plain_Text key is a non-empty string
            if not isinstance(item['Plain Text'], str) or not item['Plain Text'].strip():
                raise ValueError(f"Validation failed for item at index {idx}: Invalid or empty 'Plain_Text' value.")
        return data
    except Exception as e:
        print(f"An error occurred during schema validation: {e}")
        raise RuntimeError("Failed to validate schema.") from e
