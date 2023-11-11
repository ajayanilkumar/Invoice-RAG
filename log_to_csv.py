import PyPDF2
import sys
from time import sleep
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from llm import load_llm
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import * 
from langchain.document_loaders import PyPDFLoader
import json
import csv

csv_file_path = "/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/invoice.csv"

if __name__ == '__main__':
    directory = "/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/data/"


    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        #print(txt)
        loader = PyPDFLoader(f)

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                                    chunk_overlap=CHUNK_OVERLAP)
        texts = text_splitter.split_documents(documents)
            
        prompt_template = "Given the information about the products through this invoice. Can you give me the details of the invoice in the following JSON format? \
                            product_type: \
                            invoice_no:  \
                            total_amount: \
                            date_purchased: \
                            {invoice}        \
                            Just give me the JSON with the above keys with info, dont give me any other information."

        llm = OpenAI(temperature=0)
        llm_chain = LLMChain(llm=load_llm(), prompt=PromptTemplate.from_template(prompt_template))
        json_object = json.loads(llm_chain(texts)['text'])
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(json_object.values())

        
        sleep(3)

