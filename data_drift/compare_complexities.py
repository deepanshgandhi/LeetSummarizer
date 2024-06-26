from typing import List
from code_complexity import calculate_cyclomatic_complexity

def extract_code_and_calculate_avg(json_data: List[dict], code_field: str) -> float:
    """
    Extract code from JSON data, calculate its cyclomatic complexity, and compute the average complexity.

    Args:
    json_data (List[dict]): The JSON data containing code snippets.
    code_field (str): The field name in the JSON data where the code snippets are stored.

    Returns:
    float: The average cyclomatic complexity of the code snippets.
    """
    total_complexity = 0
    num_code_snippets = 0
    
    for item in json_data:
        if code_field in item:
            code_snippet = item[code_field]
            complexity = calculate_cyclomatic_complexity(code_snippet)
            if complexity is not None:
                total_complexity += complexity
                num_code_snippets += 1
            
    if num_code_snippets > 0:
        avg_complexity = total_complexity / num_code_snippets
        print(f"Processed {num_code_snippets} code snippets.")
        return avg_complexity
    else:
        print("No valid code snippets found.")
        return 0
