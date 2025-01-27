import json
from airflow.providers.google.cloud.hooks.gcs import GCSHook

def print_final_data(data: list, bucket_name: str, destination_blob_name: str, **kwargs) -> None:
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
    # Save to a local file
    local_path = '/tmp/preprocessed_data.json'
    with open(local_path, 'w') as f:
        json.dump(data, f)
    
    print("Uploading to GCS using GCSHook")
    upload_to_gcs_using_hook(local_path, bucket_name, destination_blob_name)

def upload_to_gcs_using_hook(local_path: str, bucket_name: str, destination_blob_name: str) -> None:
    """
    Uploads a file to a GCS bucket using GCSHook.

    Args:
    local_path (str): Path to the local file.
    bucket_name (str): Name of the GCS bucket.
    destination_blob_name (str): Destination path in the GCS bucket.

    Returns:
    None
    """
    # Initialize the GCSHook
    gcs_hook = GCSHook()
    
    # Upload the file to GCS
    gcs_hook.upload(bucket_name, destination_blob_name, local_path)
    
    print(f"File {local_path} uploaded to {destination_blob_name} in bucket {bucket_name}.")

