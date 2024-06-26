from typing import Tuple
from load_data_from_firestore import load_data
from code_complexity import calculate_cyclomatic_complexity
from compare_complexities import extract_code_and_calculate_avg

def detect_drift(avg_complexity_1: float, avg_complexity_2: float, threshold: float = 1.0) -> bool:
    """
    Detect drift between two average complexities.

    Args:
    avg_complexity_1 (float): The average complexity of the first collection.
    avg_complexity_2 (float): The average complexity of the second collection.
    threshold (float): The threshold for detecting significant drift.

    Returns:
    bool: True if drift is detected, False otherwise.
    """
    drift = abs(avg_complexity_1 - avg_complexity_2)
    print(f"Drift detected: {drift} (Threshold: {threshold})")
    return drift > threshold

def compare_complexities_and_detect_drift(collection1: str, collection2: str, field1: str, field2: str, threshold: float = 4.0) -> Tuple[float, float, bool]:
    """
    Compare the complexities of two Firestore collections and detect drift.

    Args:
    collection1 (str): The name of the first Firestore collection.
    collection2 (str): The name of the second Firestore collection.
    field1 (str): The field name in the first collection where code snippets are stored.
    field2 (str): The field name in the second collection where code snippets are stored.
    threshold (float): The threshold for detecting significant drift.

    Returns:
    Tuple[float, float, bool]: The average complexities of both collections and whether drift was detected.
    """
    data1 = load_data(collection1)
    data2 = load_data(collection2)

    avg_complexity_1 = extract_code_and_calculate_avg(data1, field1)
    avg_complexity_2 = extract_code_and_calculate_avg(data2, field2)

    drift_detected = detect_drift(avg_complexity_1, avg_complexity_2, threshold)

    return avg_complexity_1, avg_complexity_2, drift_detected

if __name__ == "__main__":
    collection1 = 'Questions'
    collection2 = 'Training_data'
    field1 = 'code'  # Field name for code snippets in 'Questions' collection
    field2 = 'Code'  # Field name for code snippets in 'Training_data' collection
    threshold = 4.0  # Define your threshold for detecting significant drift

    avg_complexity_1, avg_complexity_2, drift_detected = compare_complexities_and_detect_drift(collection1, collection2, field1, field2, threshold)
    print(f"Average Complexity - {collection1}: {avg_complexity_1}")
    print(f"Average Complexity - {collection2}: {avg_complexity_2}")
    print(f"Drift Detected: {drift_detected}")