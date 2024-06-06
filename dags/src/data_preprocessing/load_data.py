

import os
from google.cloud import  firestore


def load_data() -> list:
    """
    Load data from firestore.

    Returns:
    list: The data in the form of a list of dictionaries.
    """
    # Create your personal private key
    # Modify path accordingly. Currently file stored in model/data_preprocessing
    
    service_account_path = os.path.join(os.path.dirname(__file__), "service_account_key.json")
    print(service_account_path)
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
    # file = open('items.txt','w')
    # for item in data:
    #     file.write(item+"\n")
    # file.close()

    return data


# load_data()