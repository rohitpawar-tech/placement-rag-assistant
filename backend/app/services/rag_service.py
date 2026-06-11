import os
import shutil
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.core.config import settings

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)

class RAGService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        
        # Check if API Key exists and is valid (not empty)
        if self.api_key and self.api_key != "" and self.api_key != "your-google-gemini-api-key-here":
            print("--- Starting in REAL MODE (Using Google AI) ---")
            self.mode = "REAL"
            self.embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL, google_api_key=self.api_key)
            self.llm = ChatGoogleGenerativeAI(model=settings.CHAT_MODEL, google_api_key=self.api_key, temperature=0.7)
            self.vector_store = None
            self._load_vector_store()
        else:
            print("--- Starting in MOCK MODE (No API Key) ---")
            self.mode = "MOCK"

    def _load_vector_store(self):
        if self.mode == "MOCK": return
        
        index_path = os.path.join(settings.VECTOR_DB_DIR, "index")
        if os.path.exists(index_path):
            self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vector_store = FAISS.from_texts(["Initialize"], self.embeddings)

    def ingest_document(self, file_path: str, filename: str):
        if self.mode == "MOCK":
            print(f"[MOCK] Document {filename} ingested (Simulated).")
            return True
            
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            else:
                loader = TextLoader(file_path)
            
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(documents)

            for text in texts:
                text.metadata["source"] = filename

            if self.vector_store:
                self.vector_store.add_documents(texts)
            else:
                self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
            self.vector_store.save_local(os.path.join(settings.VECTOR_DB_DIR, "index"))
            return True
        except Exception as e:
            print(f"Error ingesting: {e}")
            return False

    def query(self, question: str, k: int = 4) -> dict:
        if self.mode == "MOCK":
            return {
                "answer": "I am running in **Mock Mode** because no API key was provided. \n\nIn this mode, I simulate a response. In a real deployment, I would search your uploaded documents using FAISS and generate a real answer with Google Gemini.",
                "sources": ["mock_document.pdf"]
            }

        if not self.vector_store:
            return {"answer": "No documents indexed yet. Please upload files.", "sources": []}

        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        
        prompt_template = """
        You are an expert Placement Preparation Assistant. 
        Use the following pieces of context to answer the question at the end.
        Context: {context}
        Question: {question}
        Answer:
        """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )

        response = chain.invoke({"query": question})
        
        sources = []
        if 'source_documents' in response:
            sources = list(set([doc.metadata.get('source', 'Unknown') for doc in response['source_documents']]))

        return {
            "answer": response['result'],
            "sources": sources
        }

rag_service = RAGService()