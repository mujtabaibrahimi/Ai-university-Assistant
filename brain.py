import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

load_dotenv()

# Create data directory if it doesn't exist
Path("./data").mkdir(exist_ok=True)

class UniversityAI:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.vector_db = None

    def ingest_notes(self, file_path):
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            if not pages:
                raise ValueError(f"No pages found in {file_path}. The PDF may be empty or corrupted.")
            
            # Check if pages have actual content
            total_content = "".join([page.page_content for page in pages])
            if not total_content.strip():
                raise ValueError(f"No text content extracted from {file_path}. The PDF may be image-only or corrupted.")
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = splitter.split_documents(pages)
            
            if not docs or not any(doc.page_content.strip() for doc in docs):
                raise ValueError(f"No valid documents created after splitting. The PDF content may be insufficient.")
            
            # Filter out empty documents
            docs = [doc for doc in docs if doc.page_content.strip()]
            
            # Clear existing database if needed
            import shutil
            if self.vector_db is not None:
                try:
                    self.vector_db.delete_collection()
                except Exception:
                    pass
                self.vector_db = None
            if os.path.exists("./chroma_db"):
                try:
                    shutil.rmtree("./chroma_db")
                except PermissionError:
                    pass  # Windows file lock; ChromaDB will reuse the directory
            
            self.vector_db = Chroma.from_documents(docs, self.embeddings, persist_directory="./chroma_db")
        except Exception as e:
            raise Exception(f"Error ingesting notes: {str(e)}")

    def get_response(self, query, mode="General"):
        if not self.vector_db:
            return "Please upload your notes first!"
        
        # Custom Prompting based on the "Teacher" feature
        if mode == "Teacher":
            prompt_template = """You are a helpful University Professor. Use the following notes to explain the concept.
Use analogies, keep it encouraging, and end with a 'knowledge check' question.

Context: {context}
Student Question: {input}

Answer:"""
        elif mode == "Exam Prep":
            prompt_template = """You are an Exam Coach. Based on the notes, identify the most important definitions 
and potential exam questions related to this topic.

Context: {context}
Student Question: {input}

Answer:"""
        else:
            prompt_template = "Answer based on context: {context}\n\nQuestion: {input}\n\nAnswer:"

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "input"])
        
        # Retrieve relevant documents
        retriever = self.vector_db.as_retriever()
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Format the prompt and get response
        formatted_prompt = PROMPT.format(context=context, input=query)
        response = self.llm.invoke(formatted_prompt)
        
        return response.content if hasattr(response, 'content') else str(response)