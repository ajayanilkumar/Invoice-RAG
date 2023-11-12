# Invoice-RAG

A project that leverages LLMs for invoice processing.
![dataflow](https://github.com/ajayanilkumar/Invoice-RAG/assets/79352659/8062150b-fb54-4032-a3a0-dc976de63c47)

We have written modular code for abstracting many of the functions.
config.py  - takes care of all the variables.
llm.py - used to load the LLM. This file can be used as a way to choose a particular LLM we want and load that particular LLM.
qachain.py - creates a retrieval qa chain.
ensemble.py - we use bm25 and FAISS vector embeddings while querying using the InvoiceBOT. This is a type of advanced RAG.
ingest.py - this is used to store the FAISS embeddings of the invoice dataset, which is loaded in ensemble.py.
vectorstore - the FAISS embeddings are stored here.
log_to_csv.py - the logic to convert the invoice data into structure CSV files via LLM.



After cloning the repo, and creating a virtual environment, run the following commands.
*Make sure you change all the path strings in the files (soory we couldnt do it in time)*

```python
pip install -r requirements.txt
python ingest.py
streamlit run homepage.py
```

While you are on the analytics page, make sure to use the invoice_cleaned.csv as the input file for generating LIDA infographics.

The data folder consists of a few invoices. We wanted to add diversity to the dataset so we used different types of invoices to see of the LLM can process it.
The results folder consists of some output screenshots.
