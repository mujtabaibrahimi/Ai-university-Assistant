# AI University Study Assistant

A RAG-powered study assistant that lets you upload lecture notes and course PDFs, then ask questions in different learning modes. Built with Streamlit, LangChain, and Groq.

## Features

- **PDF Upload & Indexing** - Upload syllabi or lecture notes and have them chunked, embedded, and stored in ChromaDB for retrieval.
- **3 Assistant Modes:**
  - **General** - Straightforward answers based on your notes.
  - **Teacher** - Explains concepts with analogies and ends with a knowledge-check question.
  - **Exam Prep** - Identifies key definitions and potential exam questions.
- **Auto Quiz Generator** - Generates multiple-choice questions from your uploaded notes with one click.

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** Llama 3.3 70B via Groq
- **Embeddings:** `all-MiniLM-L6-v2` (sentence-transformers)
- **Vector Store:** ChromaDB
- **Framework:** LangChain

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/mujtabaibrahimi/Ai-university-Assistant.git
cd Ai-university-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

```bash
streamlit run app.py
```

## Usage

1. Upload a PDF (lecture notes, syllabus, textbook chapter) via the sidebar.
2. Choose an assistant mode: General, Teacher, or Exam Prep.
3. Type your question and get answers grounded in your notes.
4. Click "Generate a Quiz from my Notes" to test yourself.

## Project Structure

```
├── app.py             # Streamlit UI
├── brain.py           # RAG pipeline (PDF ingestion, retrieval, LLM)
├── requirements.txt   # Python dependencies
├── .env               # API keys (not tracked)
└── .gitignore
```
