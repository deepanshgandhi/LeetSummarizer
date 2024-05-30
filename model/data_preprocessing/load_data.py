import os
from google.cloud import firestore

def load_data() -> list:
    """
    Load data from firestore.

    Returns:
    list: The data in the form of a list of dictionaries.
    """
    # Create your personal private key
    # Modify path accordingly. Currently file stored in model/data_preprocessing
    service_account_path = "service_account_key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

    db = firestore.Client()
    doc_ref = db.collection('Training_data').get()

    if len(doc_ref) == 0:
        print("Collection is empty!!")
    else:
        data = []
        for doc in doc_ref:
            if doc.exists:
                data.append(doc.to_dict())
            else:
                print("No such document!")
    
    return data

#load_data()