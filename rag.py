from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_chroma import Chroma


# Create Vector Store
# ------------------------------------

def create_vector_store(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Create Chroma vector database
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return vector_store


# ------------------------------------
# Ask Question
# ------------------------------------

def ask_question(vector_store, question):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )

    prompt = f"""
You are a helpful medical document assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply:
"I could not find this information in the document."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content