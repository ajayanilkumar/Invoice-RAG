from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import * 


def retriever_creation():
    loader = DirectoryLoader(DATA_DIR_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                                   chunk_overlap=CHUNK_OVERLAP)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDER,model_kwargs={'device': 'mps'})

    faiss_vectorstore = FAISS.load_local(FAISS_PATH, embeddings)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs=SEARCH_KWARGS)
    bm25_retriever = BM25Retriever.from_documents(texts)
    ensemble_retriever = EnsembleRetriever(retrievers=[faiss_retriever, bm25_retriever], weights=[0.5, 0.5])
    print("Vector Store Creation Completed")
    return ensemble_retriever

if __name__ == "__main__":
    retriever_creation()