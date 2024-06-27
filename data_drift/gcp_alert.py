import os
import json
import time
from google.cloud import firestore
from google.cloud import monitoring_v3
from drift_detection import compare_complexities_and_detect_drift

def load_data(collection_name: str) -> list:
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
    db = firestore.Client()
    doc_ref = db.collection(collection_name).get()

    if len(doc_ref) == 0:
        raise ValueError("Collection is empty!!")

    data = []
    for doc in doc_ref:
        if doc.exists:
            data.append(doc.to_dict())
        else:
            raise ValueError("No such document!")

    return data

def publish_metric(metric_name, value):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{os.getenv('leetsummarizer')}"
    series = monitoring_v3.types.TimeSeries()
    series.metric.type = f"custom.googleapis.com/drift_detected"
    series.resource.type = "global"
    point = series.points.add()
    point.value.double_value = value
    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    point.interval.end_time.seconds = seconds
    point.interval.end_time.nanos = nanos
    client.create_time_series(name=project_name, time_series=[series])

def main(event, context):
    collection1 = 'Questions'
    collection2 = 'Training_data'
    field1 = 'code'  # Field name for code snippets in 'Questions' collection
    field2 = 'Code'  # Field name for code snippets in 'Training_data' collection
    threshold = 4.0  # Define your threshold for detecting significant drift

    avg_complexity_1, avg_complexity_2, drift_detected = compare_complexities_and_detect_drift(collection1, collection2, field1, field2, threshold)
    
    print(f"Average Complexity - {collection1}: {avg_complexity_1}")
    print(f"Average Complexity - {collection2}: {avg_complexity_2}")
    print(f"Drift Detected: {drift_detected}")

    # Publish metrics to Cloud Monitoring
    publish_metric("average_complexity_questions", avg_complexity_1)
    publish_metric("average_complexity_training_data", avg_complexity_2)
    publish_metric("drift_detected", 1 if drift_detected else 0)

    return {
        "avg_complexity_questions": avg_complexity_1,
        "avg_complexity_training_data": avg_complexity_2,
        "drift_detected": drift_detected
    }
