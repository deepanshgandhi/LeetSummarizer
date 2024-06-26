from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM
import ast

app = FastAPI()


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
    print("\nLOADING BASE MODEL\n")
    base_model = AutoModelForCausalLM.from_pretrained("unsloth/mistral-7b-v0.3-bnb-4bit")
    print("\nBASE MODEL LOADED SUCCESSFULLY\n")
    print("\nLOADING OUR MODEL\n")
    model = PeftModel.from_pretrained(base_model, "deepansh1404/leetsummarizer-mistral", use_safetensors = True)
    print("\nOUR MODEL LOADED SUCCESSFULLY\n")
    print("\nLOADING TOKENIZER\n")
    tokenizer = AutoTokenizer.from_pretrained("unsloth/mistral-7b-v0.3-bnb-4bit")
    print("\nTOKENIZER LOADED SUCCESSFULLY\n")

@app.post("/generate")
async def generate_summary(request: TextRequest):
    try:
        #input_text = f"Question: {request.question}\nCode: {request.code}"
        if not is_valid_python_code(request.code):
            #Log the error
            return {"status":400, "summary": "Invalid Python code"}
        input_text = prompt + "\n Question: )" + request.question + "\n Code: )" + request.code + "\n Plain Text: )"
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
        output = model.generate(**inputs, max_new_tokens=200)
        generated_sequence = output[0]
        input_length = inputs['input_ids'].shape[1]  # Length of the input text tokens
        new_tokens = generated_sequence[input_length:]  # Exclude the input tokens

        summary = tokenizer.decode(new_tokens, skip_special_tokens=True)
        #summary = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))