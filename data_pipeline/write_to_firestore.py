import pandas as pd
import os
from google.cloud import firestore

file_path = 'Leet_Summarizer_train_data.csv'
df = pd.read_csv(file_path)

# Setting google firestore creds
service_account_path = "service_account_key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

db = firestore.Client()

def format_data(text):
    formatted_text = text.replace('\\n', '\n').replace('\\t', '\t')
    return formatted_text

# Uploading to firestore
def upload_to_firestore(df):
    for index, row in df.iterrows():
        doc_id = str(index)
        data = {
            'Question': format_data(row['Question']),
            'Code': format_data(row['Code']),
            'Plain Text': format_data(row['Plain Text'])
        }
        # print(data)
        db.collection('Training_data').document(doc_id).set(data)

upload_to_firestore(df)
