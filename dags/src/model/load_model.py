from unsloth import FastLanguageModel

def load_model_tokeniser(**kwargs):
    max_seq_length = 2048
    dtype = None  # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
    load_in_4bit = True  # Use 4bit quantization to reduce memory usage. Can be False.

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/llama-3-8b-bnb-4bit",
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=8,  # rank of LoRA
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",  # No bias added for optimal performance
        use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    # Push model and tokenizer to XCom for other tasks
    kwargs['ti'].xcom_push(key='model', value=model)
    kwargs['ti'].xcom_push(key='tokenizer', value=tokenizer)
