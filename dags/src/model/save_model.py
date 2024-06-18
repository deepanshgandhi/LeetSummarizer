import mlflow

def save_model(**kwargs):
    model_path = "outputs"
    mlflow.set_tracking_uri("MLFLOW URI")
    mlflow.start_run(run_name="model_training")

    mlflow.log_artifacts(model_path)

    mlflow.end_run()