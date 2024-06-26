from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
import ast
import logging
from fastapi.responses import PlainTextResponse
import os
from google.cloud import storage

app = FastAPI()
# Get log file path from environment variable
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
storage_client = storage.Client.from_service_account_json(credentials_path)

bucket_name = 'model-results-and-logs'

class GCFileHandler(logging.StreamHandler):
    def __init__(self, bucket, blob_name):
        super().__init__()
        self.bucket = bucket
        self.blob_name = blob_name

    def emit(self, record):
        try:
            blob = self.bucket.blob(self.blob_name)
            existing_content = blob.download_as_string() if blob.exists() else b''
            updated_content = existing_content + self.format(record).encode('utf-8') + b'\n'
            blob.upload_from_string(updated_content, content_type='text/plain')
        except Exception as e:
            self.handleError(record)

# Configure logging to use GCS
log_blob_name = 'app.log'  # Replace with your desired blob path
gc_handler = GCFileHandler(storage_client.bucket(bucket_name), log_blob_name)
gc_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
gc_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[gc_handler])

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
async def stream_logs(response: Response):
    try:
        # Fetch logs from GCS blob
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(log_blob_name)
        log_stream = blob.download_as_text()

        # Set content type and return streamed logs
        response.headers["Content-Type"] = "text/plain"
        return log_stream
    except Exception as e:
        logging.error(f"An error occurred while streaming logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not stream logs from GCS.")