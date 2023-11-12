from time import sleep
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from llm import load_llm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import * 
from langchain.document_loaders import PyPDFLoader
import json
import csv

def create_csv():
    csv_file_path = "/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/invoice.csv"
    prompt_template = "Given the information about the products through this invoice. Can you give me the details of the invoice in the following JSON format? \
                        Generalize the product_type. For example if the of product comes under : Storage, Office Supplies, product_type should be: Office Supplies. \
                        Similarly if the product is: Chairs, Furniture, the product_type should be Furniture. \
                        Similarly if the products are pizzas, cakes etc, the product_type should be Food and so on.    \
                        Just give me JSON output only, dont give me additional keys other than the below mentioned. \
                                invoice_no:  \
                                product_type: \
                                product_name: \
                                total_amount: \
                                date_purchased: \
                                {invoice} "

    llm = OpenAI(temperature=0)
    llm_chain = LLMChain(llm=load_llm(), prompt=PromptTemplate.from_template(prompt_template))
    keys_to_extract = ["invoice_no", "product_type", "product_name", "total_amount", "date_purchased"]
    directory = "data/"


    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        #print(txt)
        loader = PyPDFLoader(f)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                                    chunk_overlap=CHUNK_OVERLAP)
        texts = text_splitter.split_documents(document)
        json_object = json.loads(llm_chain(texts)['text'])
        extracted_data = {key: json_object[key] for key in keys_to_extract}
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(extracted_data.values())
        sleep(3) # To avoid rate limit error





