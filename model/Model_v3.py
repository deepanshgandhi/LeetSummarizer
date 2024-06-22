import tensorflow as tf
import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
from ctransformers import AutoTokenizer, AutoModelForCausalLM
from transformers import TFTrainingArguments, TFTrainer
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util
from google.cloud import storage
import json
import os
import matplotlib.pyplot as plt

max_seq_length = 2048
per_device_train_batch_size = 2
gradient_accumulation_steps = 4
warmup_steps = 5
max_steps = 15
bucket_name = 'airflow-dags-leetsummarizer'
data_file_path = 'dags/data/preprocessed_data.json'

def load_data_from_gcs(bucket_name, file_path):
    """Load JSON data from Google Cloud Storage"""
    # Initialize a client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(bucket_name)

    # Get the blob (file) from the bucket
    blob = bucket.blob(file_path)

    # Download blob as a string
    data = blob.download_as_string()

    # Parse the JSON data
    json_data = json.loads(data)

    return json_data

def upload_to_gcs(source_file_name, bucket_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage.

    Args:
        source_file_name (str): The path to the file to upload.
        bucket_name (str): The name of the GCS bucket.
        destination_blob_name (str): The destination path in the GCS bucket.
    """
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob object from the filepath
    blob = bucket.blob(destination_blob_name)

    # Upload the file to GCS
    blob.upload_from_filename(source_file_name)

def load_model_tokenizer():
    # model_name = 'meta-llama/Llama-2-7b-chat-hf'
    model_name = "TheBloke/Llama-2-7B-Chat-GGML"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

def prepare_data(tokenizer):
    data = load_data_from_gcs(bucket_name, data_file_path)
    EOS_TOKEN = tokenizer.eos_token
    prompt = "Summarize the provided code solution for the given problem in simple, plain English text. Explain in simple text how the code works to solve the specified problem."
    df = pd.DataFrame(data)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df["input_text"] = (
        prompt
        + "\n Question: )"
        + train_df["Question"]
        + "\n Code: )"
        + train_df["Code"]
        + "\n Plain Text: )"
        + train_df["Plain Text"]
        + EOS_TOKEN
    )

    custom_ds = pd.DataFrame()
    custom_ds["text"] = df["Question"]
    dataset = Dataset.from_pandas(custom_ds)
    return dataset, test_df, prompt

def train_model(model, tokenizer, train_data, test_df, prompt):
    trainer_args = TFTrainingArguments(
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        warmup_steps=warmup_steps,
        max_steps=max_steps,
        learning_rate=2e-4,
        logging_steps=1,
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="./outputs",
    )

    trainer = TFTrainer(
        model=model,
        args=trainer_args,
        train_dataset=train_data,
        eval_dataset=test_df,
    )

    trainer.train()

def evaluate_model(model, test_df, prompt, tokenizer):
    similarity_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    # Initialize ROUGE scorer
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    roguel_values = []
    similarity_values = []

    EOS_TOKEN = tokenizer.eos_token
    for idx in range(1, len(test_df)):
        data_point = test_df.iloc[idx]

        test_text = prompt + "\n Question: " + data_point["Question"] + "\n Code: " + data_point["Code"] + "\n Plain Text: " + EOS_TOKEN

        inputs = tokenizer(test_text, return_tensors="tf")
        outputs = model.generate(inputs["input_ids"])

        generated_text = tokenizer.decode(outputs.numpy()[0], skip_special_tokens=True)
        actual_text = data_point["Plain Text"]

        scores = scorer.score(generated_text, actual_text)
        rouge_l_score = scores['rougeL'].fmeasure
        roguel_values.append(rouge_l_score)

        embeddings1 = similarity_model.encode(generated_text, convert_to_tensor=True)
        embeddings2 = similarity_model.encode(actual_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        similarity_values.append(similarity.item())

    return roguel_values, similarity_values

def save_and_upload_model(model, tokenizer, gcs_model_folder, bucket_name):
    # Save TensorFlow model and tokenizer locally
    model.save_pretrained("./")  # Save in the current working directory
    tokenizer.save_pretrained("./")  # Save in the current working directory

    # Upload each file in the model directory to GCS
    for file_name in ["config.json", "tf_model.h5", "tokenizer.json"]:
        source_file_path = os.path.join("./", file_name)
        destination_blob_name = os.path.join(gcs_model_folder, file_name)
        upload_to_gcs(source_file_path, bucket_name, destination_blob_name)

if __name__ == "__main__":
    model, tokenizer = load_model_tokenizer()
    dataset, test_df, prompt = prepare_data(tokenizer)
    train_model(model, tokenizer, dataset, test_df, prompt)
    rouge_scores, similarity_scores = evaluate_model(model, test_df, prompt, tokenizer)
    save_and_upload_model(model, tokenizer, "dags/model/model_dump/", bucket_name)
