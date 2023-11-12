import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Invoice-GPT"
)
st.header('Welcome to Invoice-GPT!')
st.sidebar.success("Select a page below")

st.write('This is an app designed to take care of invoice processing in companies.\n')

image = Image.open('/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/homeImage.jpeg')
st.image(image, use_column_width=True)

st.subheader('There are 3 parts in this application :')
st.write('Part 1: Chat with your invoice using advanced RAG - get details about any invoice by quickly querying in natural language.\n')
st.write('Part 2: Created structured data from your invoice - use LLM to find the required fields from the invoice and append it to a CSV file\n')
st.write('Part 3: Create infographics to analyse spendings using LIDA - use the CSV files generated and feed it into Microsoft LIDA for visualization.\n\n')

