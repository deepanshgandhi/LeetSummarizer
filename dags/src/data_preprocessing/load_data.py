import os
from google.cloud import firestore

def load_data() -> list:
    """
    Load data from Firestore.

    Returns:
    list: The data in the form of a list of dictionaries.
    """
    service_account_path = os.path.join(os.path.dirname(__file__), "service_account_key.json")
    print(service_account_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

    try:
        db = firestore.Client()
        doc_ref = db.collection('Training_data').get()

        if len(doc_ref) == 0:
            raise ValueError("Collection is empty!!")

        data = []
        for doc in doc_ref:
            if doc.exists:
                data.append(doc.to_dict())
            else:
                raise ValueError("No such document!")
    except Exception as e:
        raise RuntimeError("Failed to load data from Firestore.") from e

    return data