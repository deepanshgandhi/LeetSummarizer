import torch
import mlflow
import mlflow.pytorch
import pandas as pd
from peft import LoraConfig, get_peft_model
from transformers import TrainingArguments
from trl import SFTTrainer
import warnings
from datasets import Dataset
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
warnings.filterwarnings("ignore")

def install_packages():
    # !pip install -q -U trl transformers accelerate git+https://github.com/huggingface/peft.git
    # !pip install -q datasets bitsandbytes einops wandb
    pass

def login_huggingface(token):    
    login(token)

def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

def preprocess_data(df):
    df["question"] = (
        df["Prompt"]
        + "\n Question: )"
        + df["Question"]
        + "\n Code: )"
        + df["Code"]
        + "\n Plain Text: )"
    )
    custom_ds = pd.DataFrame()
    custom_ds["prompt"] = df["question"]
    from datasets import Dataset
    dataset = Dataset.from_pandas(custom_ds)
    return dataset

def load_model_and_tokenizer(model_name):
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, trust_remote_code=True)
    model.config.use_cache = False
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def configure_peft(lora_alpha=16, lora_dropout=0.1, lora_r=64):
    peft_config = LoraConfig(
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=lora_r,
        bias="none",
        task_type="CAUSAL_LM",
    )
    return peft_config

def create_training_arguments(output_dir="./results", per_device_train_batch_size=4, gradient_accumulation_steps=4, 
                              optim="paged_adamw_32bit", save_steps=200, logging_steps=10, learning_rate=2e-4, 
                              max_grad_norm=0.3, max_steps=10, warmup_ratio=0.03, lr_scheduler_type="constant"):
    training_arguments = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim=optim,
        save_steps=save_steps,
        logging_steps=logging_steps,
        learning_rate=learning_rate,
        fp16=True,
        max_grad_norm=max_grad_norm,
        max_steps=max_steps,
        warmup_ratio=warmup_ratio,
        group_by_length=True,
        lr_scheduler_type=lr_scheduler_type,
    )
    return training_arguments

def train_model(model, dataset, peft_config, tokenizer, training_arguments, max_seq_length=512):
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        dataset_text_field="prompt",
        max_seq_length=max_seq_length,
        tokenizer=tokenizer,
        args=training_arguments,
    )
    for name, module in trainer.model.named_modules():
        if "norm" in name:
            module = module.to(torch.float32)
    trainer.train()
    return trainer

def save_model(trainer, output_path="outputs"):
    model_to_save = trainer.model.module if hasattr(trainer.model, 'module') else trainer.model
    model_to_save.save_pretrained(output_path)

def load_trained_model(model, output_path="outputs"):
    lora_config = LoraConfig.from_pretrained(output_path)
    model = get_peft_model(model, lora_config)
    return model

def generate_text(model, tokenizer, test_df):
    test_row = test_df.head(1)
    test_text = test_row["Prompt"].values[0] + "\n Question: )" + test_row["Question"].values[0] + "\n Code: )" + test_row["Code"].values[0] + "\n Plain Text: )"
    print(test_text)
    input_ids = tokenizer.encode(test_text, return_tensors="pt", max_length=1024, truncation=True)
    with torch.no_grad():
        output = model.generate(input_ids, max_length=400, num_return_sequences=1)
    for i, seq in enumerate(output):
        generated_text = tokenizer.decode(seq, skip_special_tokens=True)
        print(f"Generated text {i+1}: {generated_text}")


def main():
    mlflow.start_run()  # Start MLFlow run

    try:
        install_packages()
        login_huggingface("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")
        train_df = load_data('train.xlsx')
        dataset = preprocess_data(train_df)
        model_name = "meta-llama/Llama-2-7b-chat-hf"
        model, tokenizer = load_model_and_tokenizer(model_name)
        peft_config = configure_peft()
        training_arguments = create_training_arguments()
        trainer = train_model(model, dataset, peft_config, tokenizer, training_arguments)
        save_model(trainer)
        model = load_trained_model(model)
        test_df = load_data('test.xlsx')
        generate_text(model, tokenizer, test_df)
    
        # Log model and parameters
        mlflow.pytorch.log_model(model, "model")
        mlflow.log_params({
            "lora_alpha": 16,
            "lora_dropout": 0.1,
            "lora_r": 64,
            "learning_rate": 2e-4,
            "max_steps": 10
        })

    finally:
        mlflow.end_run()  # End the MLFlow run

if __name__ == "__main__":
    main()

