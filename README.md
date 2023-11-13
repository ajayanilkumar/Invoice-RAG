# Invoice-RAG

A project that leverages LLMs for invoice processing.
![dataflow](https://github.com/ajayanilkumar/Invoice-RAG/assets/79352659/8062150b-fb54-4032-a3a0-dc976de63c47)

Invoice-RAG is a project that utilizes Large Language Models (LLMs) for efficient invoice processing. Traditionally, analyzing a large volume of invoices is cumbersome and manually intensive. Our AI-driven application streamlines this process by allowing users to upload their Invoice PDFs, and the application does the rest.

## Features

- **Chat with Your Invoice PDFs**: Interact with your invoices through a chat interface. Ask questions in natural language and receive answers without the need to sift through multiple PDFs manually.
- **Automated CSV Conversion**: Convert invoice data into structured CSV files automatically. Simply upload your invoice PDFs, and our application will extract the relevant information.
- **Visualize Your Data**: With LIDA integration, create custom visualizations to gain insights into spending patterns. Users can generate custom graphs through natural language queries, eliminating the need for a data analyst.

## Modular Codebase

- `config.py`: Manages all the variables.
- `llm.py`: Handles the loading of the chosen LLM.
- `qachain.py`: Creates a retrieval QA chain.
- `ensemble.py`: Utilizes bm25 and FAISS vector embeddings for advanced retrieval augmented generation (RAG).
- `ingest.py`: Stores FAISS embeddings of the invoice dataset, loaded in `ensemble.py`.
- `vectorstore`: Stores the FAISS embeddings.
- `log_to_csv.py`: Converts invoice data into structured CSV files using LLM.

## Getting Started

After cloning the repository and setting up a virtual environment, execute the following commands:

```shell
pip install -r requirements.txt
python ingest.py
streamlit run homepage.py
```

While you are on the analytics page, make sure to use the invoice_cleaned.csv as the input file for generating LIDA infographics.

The data folder consists of a few invoices. We wanted to add diversity to the dataset so we used different types of invoices to see if the LLM can process it.
The results folder consists of some output screenshots.
