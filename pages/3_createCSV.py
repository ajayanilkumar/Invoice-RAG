import streamlit as st
import sys
sys.path.insert(1, '/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/log_to_csv.py')
from log_to_csv import create_csv
from PIL import Image

st.title("Invoice to structured data in CSV")

st.header('Why use LLMs?')
st.write('Current solutions used to extract data from invoices include NER, computer vision, and custom keyword searching.\n')
st.write('While these methods can be accurate for the given task, it can easily become outdated if new type of information/data from the invoice has to be extracted.\n')
st.write('When this happens, the solution must be modified to capture the new required data.\n')
st.write('To avoid these issues, we can use LLMs to extract the required data from the invoice and convert it into a structured format for further analysis.\n')
st.write('Furthermore LLMs can be re-used for other tasks within the company.\n')


def on_button_clicked():
    create_csv()

st.subheader("Click on the button below to generate CSV file by extracting details from every invoice.")
st.write("On clicking the below button, an LLM chain is created, and each invoice-PDF is iterated over and read by the LLM.\n")
st.write("The LLM gives us the required fields as a JSON object which is then appended to the CSV file.\n")


if st.button('Generate CSV'):
    on_button_clicked()

st.subheader('Example of a CSV created from the dataset.')


image = Image.open('/Users/anilrao/Desktop/RAG_PROJECTS/Invoice/exampleCSV.png')
st.image(image, caption='InvoiceCSV', use_column_width=True)