DATA_DIR_PATH = "data/"
FAISS_PATH = "vectorstore/faiss/"
CHUNK_SIZE = 250
CHUNK_OVERLAP = 50
EMBEDDER = "BAAI/bge-base-en-v1.5"
DEVICE = "mps"
PROMPT_TEMPLATE = '''
You are my invoice analyzer. You are great at anaylyzing the invoice and giving me the information I require by answering the question.
If you cant answer the question based on the information either say you cant find an answer or don't answer at all.


Context: {context}
Question: {question}
Do provide only helpful answers

Helpful answer:
'''
INP_VARS = ['context', 'question']
CHAIN_TYPE = "stuff"
SEARCH_KWARGS = {'k': 2}
#MODEL_CKPT = "res/mistral-7b-openorca.Q8_0.gguf"
#MODEL_TYPE = "llama"
MAX_NEW_TOKENS = 100
TEMPERATURE = 0.0