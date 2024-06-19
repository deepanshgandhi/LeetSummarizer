import torch
import matplotlib.pyplot as plt
from rouge_score import rouge_scorer
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer, util
from unsloth import FastLanguageModel

def evaluate_model(**kwargs):
    model_path = kwargs['ti'].xcom_pull(key='model_directory', task_ids='save_model')
    test_df = kwargs['ti'].xcom_pull(key='test_data', task_ids='train_model')
    # Load the model from the model_directory
    model = FastLanguageModel.from_pretrained(model_path)
    similarity_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    # Assuming test_df is a pandas DataFrame where each row represents a data point
    roguel_values = []
    similarity_values = []
    model.eval()  # Set the model to evaluation mode

    # Initialize ROUGE scorer
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    # Iterate over each row in test_df, skipping the first row (index 0)
    for idx in range(1, len(test_df)):
        data_point = test_df.iloc[idx]
        with torch.no_grad():
            test_text = prompt + "\n Question: " + data_point["Question"] + "\n Code: " + data_point["Code"] + "\n Plain Text: " + EOS_TOKEN
            
            # Tokenize and encode the test_text
            inputs = tokenizer([test_text], return_tensors="pt").to("cuda")
            
            # Generate text using the model
            outputs = model.generate(**inputs, max_new_tokens=200)

            generated_sequence = outputs[0]
            input_length = inputs['input_ids'].shape[1]  # Length of the input text tokens
            new_tokens = generated_sequence[input_length:]  # Exclude the input tokens

            generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)
            
            # Decode the generated sequence
            #generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            actual_text = data_point["Plain Text"]
            
            # Compute ROUGE scores
            scores = scorer.score(generated_text, actual_text)
            
            # ROUGE-L score can be used as a single metric for evaluation
            rouge_l_score = scores['rougeL'].fmeasure
            
            # Append ROUGE-L score to test_loss_values
            roguel_values.append(rouge_l_score)
            embeddings1 = similarity_model.encode(generated_text, convert_to_tensor=True)
            embeddings2 = similarity_model.encode(actual_text, convert_to_tensor=True)

            similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
            similarity_values.append(similarity.item())

    # Plot the ROUGE-L scores
    plt.figure(figsize=(10, 5))
    plt.plot(roguel_values, label='ROUGE-L Score')
    plt.xlabel('Data Point')
    plt.ylabel('ROUGE-L Score')
    plt.title('ROUGE-L Score per Data Point')
    plt.xticks(range(len(roguel_values)), [f'Data {i+1}' for i in range(len(roguel_values))])
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot the similarity scores
    plt.figure(figsize=(10, 5))
    plt.plot(similarity_values, label='Similarity Score')
    plt.xlabel('Data Point')
    plt.ylabel('Similarity Score')
    plt.title('Similarity Score per Data Point')
    plt.xticks(range(len(similarity_values)), [f'Data {i+1}' for i in range(len(similarity_values))])
    plt.legend()
    plt.grid(True)
    plt.show()