import pandas as pd
from datasets import Dataset
from unsloth import is_bfloat16_supported
from trl import SFTTrainer
from transformers import TrainingArguments
from sklearn.model_selection import train_test_split
from datetime import datetime
import os


def prepare_dataset(**kwargs):
    model = kwargs['ti'].xcom_pull(key='model', task_ids='load_model_tokenizer')
    tokenizer = kwargs['ti'].xcom_pull(key='tokenizer', task_ids='load_model_tokenizer')
    data = kwargs['ti'].xcom_pull(key='data', task_ids='load_model_tokenizer')
    EOS_TOKEN = tokenizer.eos_token
    prompt = "Summarize the provided code solution for the given problem in simple, plain English text. Explain in simple text how the code works to solve the specified problem."

    # Create a DataFrame from the input data
    df = pd.DataFrame(data)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df["question"] = (
        prompt
        + "\n Question: )"
        + train_df["Question"]
        + "\n Code: )"
        + train_df["Code"]
        + "\n Plain Text: )"
        + train_df["Plain_Text"]
        + EOS_TOKEN
    )

    custom_ds = pd.DataFrame()
    custom_ds["text"] = df["question"]
    dataset = Dataset.from_pandas(custom_ds)

    # Push dataset to XCom for other tasks
    kwargs['ti'].xcom_push(key='train_data', value=dataset)
    kwargs['ti'].xcom_push(key='test_data', value=test_df)
    kwargs['ti'].xcom_push(key='prompt', value=prompt)

def train_model(**kwargs):
    model = kwargs['ti'].xcom_pull(key='model', task_ids='load_model_tokenizer')
    tokenizer = kwargs['ti'].xcom_pull(key='tokenizer', task_ids='load_model_tokenizer')
    train_data = kwargs['ti'].xcom_pull(key='train_data', task_ids='prepare_dataset')
    test_df = kwargs['ti'].xcom_pull(key='test_data', task_ids='prepare_dataset')
    prompt = kwargs['ti'].xcom_pull(key='prompt', task_ids='prepare_dataset')
    max_seq_length = 2048

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_data,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=15,
            learning_rate=2e-4,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir="outputs",
        ),
    )

    trainer.train()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a unique directory name with the datetime stamp
    save_directory = os.path.join("outputs", f"model_{now}")

    # Save the model to the unique directory
    trainer.save_model(save_directory)
    #trainer.save_model("outputs")
    kwargs['ti'].xcom_push(key='model_directory', value=save_directory)
    kwargs['ti'].xcom_push(key='test_data', value=test_df)
    kwargs['ti'].xcom_push(key='prompt', value=prompt)