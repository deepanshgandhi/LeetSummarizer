from typing import List
from load_train_data import load_train_code
from code_complexity import calculate_cyclomatic_complexity

def extract_code_and_calculate_avg(json_data: List[dict]) -> float:
    total_complexity = 0
    num_code_snippets = 0
    
    for item in json_data:
        if 'Code' in item:
            code_snippet = item['Code']
            complexity = calculate_cyclomatic_complexity(code_snippet)
            if complexity is not None:
                total_complexity += complexity
                num_code_snippets += 1
    
    if num_code_snippets > 0:
        avg_complexity = total_complexity / num_code_snippets
        return avg_complexity
    else:
        return 0  # Default to 0 if no valid code snippets found

# Calculate average cyclomatic complexity for the code snippets in json_data
json_data = load_train_code()
avg_complexity = extract_code_and_calculate_avg(json_data)
print(f"Average Cyclomatic Complexity: {avg_complexity}")
