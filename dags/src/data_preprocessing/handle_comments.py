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
    print(cleaned_code)
    return cleaned_code


def handle_comments(data : list) -> list:
    
    for i in data:
        print(i['Code'])


# remove_comments('class Solution:\r\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\r\n        prevMap = {}  # val -> index\r\n\r\n        for i, n in enumerate(nums):\r\n            diff = target - n\r\n            if diff in prevMap:\r\n                return [prevMap[diff], i]\r\n            prevMap[n] = i')