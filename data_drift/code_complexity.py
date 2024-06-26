import ast

def calculate_cyclomatic_complexity(code: str) -> int:
    try:
        # Parse the code into an abstract syntax tree (AST)
        parsed_code = ast.parse(code)
        
        # Initialize complexity count
        complexity = 1  # Start with 1 for the main function entry
        
        # Helper function to recursively traverse the AST
        def traverse(node):
            nonlocal complexity
            
            if isinstance(node, ast.If) or isinstance(node, ast.For) or \
               isinstance(node, ast.While) or isinstance(node, ast.With):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                complexity += 1  # Each function definition adds 1 to complexity
            
            for child_node in ast.iter_child_nodes(node):
                traverse(child_node)
        
        # Traverse the AST to calculate complexity
        traverse(parsed_code)
        
        return complexity
    
    except SyntaxError:
        return None