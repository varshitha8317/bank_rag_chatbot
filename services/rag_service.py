from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load once
loader = TextLoader("data/bank_faq.txt")
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
docs = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()
db_vector = FAISS.from_documents(docs, embeddings)

retriever = db_vector.as_retriever()


def get_answer(query):
    docs = retriever.invoke(query)

    if not docs:
        return "I don't know"

    return docs[0].page_content