import apache_beam as beam
from apache_beam.io.gcp.bigquery import BigQuerySource, BigQuerySink
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions

# Define pipeline options
pipeline_options = PipelineOptions()
google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
google_cloud_options.project = 'my_project'
google_cloud_options.job_name = 'filter-logs-job'
google_cloud_options.region = 'us-central1'
pipeline_options.view_as(GoogleCloudOptions)

# Define the pipeline
with beam.Pipeline(options=pipeline_options) as pipeline:
    # Read from BigQuery
    logs = (
        pipeline
        | 'ReadFromBigQuery' >> beam.io.Read(BigQuerySource(query='SELECT * FROM `leetsummarizer.project_logging.logs`', use_standard_sql=True))
    )

# Define the schema for BigQuery
schema = (
    'logName:STRING,'
    'resource_type:STRING,'
    'resource_labels_instance_id:STRING,'
    'resource_labels_zone:STRING,'
    'resource_labels_project_id:STRING,'
    'timestamp:TIMESTAMP,'
    'severity:STRING'
)

# Filter and transform data
filtered_logs = (
    logs
    | 'FilterColumns' >> beam.Map(lambda row: {
        'logName': row['logName'],
        'resource_type': row['resource']['type'],
        'resource_labels_instance_id': row['resource']['labels']['instance_id'],
        'resource_labels_zone': row['resource']['labels']['zone'],
        'resource_labels_project_id': row['resource']['labels']['project_id'],
        'timestamp': row['timestamp'],
        'severity': row['severity']
    })
)

# Write to BigQuery
filtered_logs | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
    'leetsummarizer.project_logging.logs_filtered',
    schema=schema,
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
)