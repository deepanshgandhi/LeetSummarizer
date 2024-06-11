from google.cloud import firestore
import json
import os

def fetch_firestore_data():
    service_account_path = "service_account_key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
    db = firestore.Client()
    collection_ref = db.collection('Training_data')
    docs = collection_ref.stream()
    data = [doc.to_dict() for doc in docs]

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    fetch_firestore_data()
