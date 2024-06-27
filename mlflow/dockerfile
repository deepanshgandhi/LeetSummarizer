FROM python:3.9.18-slim

WORKDIR /mlflow

RUN pip install mlflow

# Create an empty SQLite database file
RUN touch /mlflow/mlflow.db

# Verify that the file is created and writable
RUN ls -la /mlflow && chmod 777 /mlflow/mlflow.db

# Set permissions for the mlruns directory
RUN mkdir -p /mlflow/artifacts && chmod -R 777 /mlflow

EXPOSE 5000

# CMD mlflow server --backend-store-uri sqlite:////mlflow/mlflow.db

CMD mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /mlflow/artifacts \
    --artifacts-destination /mlflow/artifacts \
    --host 0.0.0.0