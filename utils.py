# import torch
# from transformers import BertForQuestionAnswering, BertTokenizer
# import os
# from pdfminer.high_level import extract_text
# import streamlit as st

# # Load the pre-trained BERT model and tokenizer
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertForQuestionAnswering.from_pretrained('bert-base-uncased')

# # Load documents from local directory
# def load_docs(directory):
#     documents = {}
#     for filename in os.listdir(directory):
#         if filename.endswith('.pdf'):
#             filepath = os.path.join(directory, filename)
#             with open(filepath, 'rb') as file:
#                 text = extract_text(file)
#                 documents[filename] = text
#     return documents

# # Store the loaded documents in a global variable
# documents = load_docs('./pdf')

# def find_match(input_query):
#     # Implement logic to find matches using the BERT model locally
#     # For now, we will search for the most relevant text snippet in the documents
#     best_match = ""
#     max_score = float('-inf')
#     for doc_name, text in documents.items():
#         inputs = tokenizer(text, input_query, return_tensors='pt', truncation=True, padding=True)
#         outputs = model(**inputs)
#         answer_start = torch.argmax(outputs.start_logits)
#         answer_end = torch.argmax(outputs.end_logits) + 1
#         answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
#         score = torch.max(outputs.start_logits).item() + torch.max(outputs.end_logits).item()
#         if score > max_score:
#             max_score = score
#             best_match = answer
#     return best_match

# def get_conversation_string():
#     conversation_string = ""
#     for i in range(len(st.session_state['responses']) - 1):
#         conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
#         conversation_string += "Bot: " + st.session_state['responses'][i + 1] + "\n"
#     return conversation_string
import os
import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer, util

# Load BERT model and tokenizer for QA
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Load SentenceTransformer model for context similarity
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def load_docs(directory):
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            text = extract_text(filepath)
            documents[filename] = text
    return documents

# Load documents from local directory and store them in a global variable
documents = load_docs('./pdf')

def find_match(input_query):
    query_embedding = embedder.encode(input_query, convert_to_tensor=True)
    best_match = ""
    highest_score = float('-inf')
    
    for doc_name, text in documents.items():
        # Split the text into chunks to avoid exceeding token limit
        chunks = [text[i:i+512] for i in range(0, len(text), 512)]
        
        for chunk in chunks:
            chunk_embedding = embedder.encode(chunk, convert_to_tensor=True)
            score = util.pytorch_cos_sim(query_embedding, chunk_embedding)[0][0].item()
            
            if score > highest_score:
                highest_score = score
                best_match = chunk
    
    return best_match

def generate_response(prompt):
    inputs = tokenizer.encode_plus(prompt, return_tensors='pt', truncation=True, max_length=512)
    input_ids = inputs['input_ids'].tolist()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(text_tokens[answer_start:answer_end])
    return answer
