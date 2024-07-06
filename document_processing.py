# In main_script.py

# import os
# from pdfminer.high_level import extract_text

# def load_docs(directory):
#     documents = {}
#     for filename in os.listdir(directory):
#         if filename.endswith('.pdf'):
#             filepath = os.path.join(directory, filename)
#             with open(filepath, 'rb') as file:
#                 text = extract_text(file)
#                 documents[filename] = text
#     return documents

import os
from pdfminer.high_level import extract_text

def load_docs(directory):
    documents = {}
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as file:
                text = extract_text(file)
                documents[filename] = text
    return documents

