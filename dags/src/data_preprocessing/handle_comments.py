def remove_comments(data: list) -> list:
    """
    Remove comments from the code in the data.

    Args:
    data (list): List of dictionaries containing 'Question', 'Code', and 'Plain_Text' keys.

    Returns:
    list: List of dictionaries with comments removed from the 'Code' key.
    """
    for item in data:
        code = item.get('Code', '')
        lines = code.split('\n')
        clean_lines = []
        for line in lines:
            if not line.strip().startswith('#'):
                clean_lines.append(line)
        clean_code = '\n'.join(clean_lines)
        item['Code'] = clean_code
    return data
