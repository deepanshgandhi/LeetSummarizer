from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
import ast
import logging
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()
# Get log file path from environment variable
log_file_path = os.getenv('LOG_FILE', 'app.log')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file_path), logging.StreamHandler()])

prompt = "Summarize the provided code solution for the given problem in simple, plain English text. Explain in simple text how the code works to solve the specified problem."
class TextRequest(BaseModel):
    question: str
    code: str

def is_valid_python_code(code):
    """
    Checks if the given Python code has valid syntax.

    Parameters:
    code (str): The Python code to check.

    Returns:
    bool: True if the code is valid, False otherwise.
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

@app.on_event("startup")
async def load_model():
    global model, tokenizer
    #config = PeftConfig.from_pretrained("deepansh1404/leetsummarizer")
    logging.info("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained("unsloth/mistral-7b-v0.3-bnb-4bit")
    logging.info("Base model loaded successfully.")
    logging.info("Loading our model...")
    model = PeftModel.from_pretrained(base_model, "deepansh1404/leetsummarizer-mistral", use_safetensors = True)
    logging.info("Our model loaded successfully.")
    logging.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("unsloth/mistral-7b-v0.3-bnb-4bit")
    logging.info("Tokenizer loaded successfully.")

@app.post("/generate")
async def generate_summary(request: TextRequest):
    logging.info(f"Question: {request.question}")
    logging.info(f"Code: {request.code}")
    try:
        #input_text = f"Question: {request.question}\nCode: {request.code}"
        if not is_valid_python_code(request.code):
            logging.error("Invalid Python code received.")
            return {"status":400, "summary": "Invalid Python code"}
        input_text = prompt + "\n Question: )" + request.question + "\n Code: )" + request.code + "\n Plain Text: )"
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        output = model.generate(**inputs, max_new_tokens=200)
        generated_sequence = output[0]
        input_length = inputs['input_ids'].shape[1]  # Length of the input text tokens
        new_tokens = generated_sequence[input_length:]  # Exclude the input tokens

        summary = tokenizer.decode(new_tokens, skip_special_tokens=True)
        logging.info(f"Generated Summary: {summary}")
        return {"status":200, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs():
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.read()
        return {"logs": logs}
    except Exception as e:
        logging.error(f"An error occurred while reading the log file: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not read log file.")