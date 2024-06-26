import datetime
from google.cloud import bigquery
from elasticsearch import Elasticsearch

# Initialize BigQuery client
client = bigquery.Client()

# Initialize Elasticsearch client
es = Elasticsearch(
    cloud_id='My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQwNDc4MDVmM2JmYzE0YTA2OGU4MzM5NjdiOTQwMWQ1MyQ2YzA2MWJiNzM3Mjg0MzYxYjFlZWIyYWZjNjQwNTA2Nw==',
    basic_auth=('odedra.r@northeastern.edu', 'leetsummarizer@1')
)

# Define your time range for fetching logs
end_time = datetime.datetime.now(datetime.timezone.utc)
start_time = end_time - datetime.timedelta(hours=1)

# Define the BigQuery query
query = """
SELECT
    timestamp,
    hardware.cpu_usage AS cpu_usage,
    hardware.gpu_usage AS gpu_usage,
    credits_used,
    error_count,
    avg_response_time,
    max_response_time
FROM
    `leetsummarizer.project_logging`
WHERE
    WHERE timestamp >= @start_time AND timestamp < @end_time
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("start_time", "TIMESTAMP", start_time),
        bigquery.ScalarQueryParameter("end_time", "TIMESTAMP", end_time),
    ]
)

# Run the query
query_job = client.query(query, job_config=job_config)
results = query_job.result()

# Index results into Elasticsearch
for row in results:
    doc = {
        "timestamp": row.timestamp,
        "log_message": row.log_message,
    }
    es.index(index="my-index", document=doc)

print("Logs successfully indexed to Elasticsearch.")
