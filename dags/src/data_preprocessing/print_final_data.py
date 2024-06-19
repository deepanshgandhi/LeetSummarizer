import json

def print_final_data(data: list) -> None:
    """
    Prints the final cleaned data

    Args:
    data (list): List of dictionaries containing 'Question', 'Code', and 'Plain_Text' keys.

    Returns:
    None
    """
    for item in data:
        code = item.get('Code', '')
        question = item.get('Question','')
        summary = item.get('Plain Text','')
        print("Question:-")
        print(question)
        print("-"*100)
        print("Code:-")
        print(code)
        print("-"*100)
        print("Plain Text:-")
        print(summary)
        print("-"*100)
        print()
        print("-"*100)
    print("Saving data in json format")
    with open('preprocessed_data.json', 'w') as f:
        json.dump(data, f)


