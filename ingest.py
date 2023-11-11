from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.retrievers import BM25Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from config import * 
import pickle


# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_DIR_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                                   chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDER,
                                       model_kwargs={'device': 'mps'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(FAISS_PATH)


if __name__ == "__main__":
    create_vector_db()

