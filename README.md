# 🎓 College AI Assistant — RAG Application

An AI-powered College Knowledge Assistant that answers user questions using information retrieved from college PDF documents. The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant document content from ChromaDB and generate context-based answers using the Groq LLM API.

## 📌 Project Overview

The College AI Assistant allows users to ask questions about college information, including academic details, admissions, placements, and other information available in the uploaded PDF documents.

Instead of sending the entire PDF to the language model for every question, the application retrieves the most relevant text chunks from a vector database and uses them as context to generate an answer.

## ✨ Features

- 📄 Supports multiple college PDF documents.
- 🔍 Semantic search using vector embeddings.
- 🧠 Retrieval-Augmented Generation (RAG) architecture.
- 💾 Persistent vector storage using ChromaDB.
- 🤖 AI-generated answers using the Groq API.
- 🖥️ Interactive frontend built with Streamlit.
- ⚙️ Flask REST API backend.
- 📚 Displays source PDF filenames and page numbers.
- 🔐 Environment-variable-based API key configuration.
- 🚫 Designed to respond based on retrieved document context.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Frontend user interface |
| Flask | Backend REST API |
| ChromaDB | Vector database |
| Sentence Transformers | Text embedding generation |
| PyMuPDF | PDF text extraction |
| Groq API | Large Language Model (LLM) |
| OpenAI Python SDK | API client compatible with Groq's endpoint |
| python-dotenv | Environment variable management |
| Requests | Frontend-to-backend communication |

## 🏗️ System Architecture

```text
              College PDF Documents
                       |
                       v
                  PDF Extraction
                       |
                       v
                  Text Chunking
                       |
                       v
              Sentence Transformer
                       |
                       v
                  Embeddings
                       |
                       v
                    ChromaDB
                       |
                       |
User Question --> Streamlit Frontend
                       |
                       v
                   Flask API
                       |
                       v
             Question Embedding
                       |
                       v
              ChromaDB Retrieval
                       |
                       v
              Relevant PDF Chunks
                       |
                       v
                   Groq LLM
                       |
                       v
                Generated Answer
                       |
                       v
                 Streamlit UI
```

## 📂 Project Structure

```text
college_rag/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── rag.py
│   ├── ingest.py
│   │
│   ├── data/
│   │   ├── college.pdf
│   │   ├── admission.pdf
│   │   └── placement.pdf
│   │
│   └── chroma_db/
│
├── frontend/
│   └── streamlit_app.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** PDF filenames are examples. Add your own PDF documents to `backend/data/`. The `chroma_db/` directory is generated when the knowledge base is created.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

Or in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

Replace `your_groq_api_key` with your own API key from the [Groq Console](https://console.groq.com/).

**Security:** Never commit your `.env` file or expose your API key in source code, screenshots, or public repositories.

### 5. Add PDF Documents

Place your college PDF documents inside:

```text
backend/data/
```

For example:

```text
backend/data/
├── college.pdf
├── admission.pdf
└── placement.pdf
```

The ingestion script processes all PDF files in this directory.

### 6. Build the Vector Database

From the project root, run:

```bash
python backend/ingest.py
```

This script:

1. Finds PDF files in the data directory.
2. Extracts text and page numbers using PyMuPDF.
3. Splits text into smaller chunks.
4. Generates embeddings using Sentence Transformers.
5. Stores the chunks, embeddings, and source metadata in ChromaDB.

Run ingestion again after adding, removing, or replacing PDFs to rebuild the knowledge base.

**Important:** The provided ingestion script recreates its collection when run, so it reprocesses the PDFs in the data directory rather than incrementally adding only new documents.

## 🚀 Running the Application

### Step 1: Start the Flask Backend

Open a terminal in the project root and run:

```bash
python backend/app.py
```

The Flask server should start at:

```text
http://127.0.0.1:5000
```

Health-check endpoint:

```text
http://127.0.0.1:5000/health
```

### Step 2: Start the Streamlit Frontend

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run frontend/streamlit_app.py
```

Open the URL displayed in the terminal, usually:

```text
http://localhost:8501
```

### Step 3: Ask Questions

Enter a question about information contained in your college PDFs.

Example questions:

- What departments are available in the college?
- What is the admission procedure?
- What courses are offered by the college?
- What placement information is available?
- Which documents are required for admission?

The application retrieves relevant PDF content and displays a generated answer along with the source document and page numbers, when available.

## 🔄 How RAG Works

**1. Retrieval:** The user's question is converted into an embedding, and ChromaDB searches for semantically similar document chunks.

**2. Augmentation:** The retrieved chunks are added to the prompt as context for the language model.

**3. Generation:** The Groq language model generates a natural-language answer using the provided context.

```text
User Question
     |
     v
Question Embedding
     |
     v
ChromaDB Similarity Search
     |
     v
Relevant Document Chunks
     |
     v
Context + User Question
     |
     v
Groq Language Model
     |
     v
Context-Based Answer
```

## 🧩 Main Modules

### `backend/ingest.py`

Processes multiple PDFs, extracts text, creates chunks and embeddings, and stores the results in ChromaDB.

### `backend/rag.py`

Handles question embeddings, semantic retrieval, context preparation, LLM calls, and source metadata.

### `backend/app.py`

Provides Flask endpoints for the application, including health checks and question answering.

### `backend/config.py`

Loads API credentials and model configuration from environment variables.

### `frontend/streamlit_app.py`

Provides the interactive user interface for submitting questions and viewing answers and sources.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running |
| GET | `/health` | Returns backend health status |
| POST | `/ask` | Retrieves relevant PDF content and generates an answer |

Example request to `/ask`:

```json
{
  "question": "What is the course outcome?"
}
```

Example response:

```json
{
  "answer": "The course outcome is described in the college documents.",
  "sources": [
    {
      "file": "curriculum.pdf",
      "page": 12
    }
  ]
}
```

The answer and source entries shown above are illustrative; actual results depend on the PDF content.

## 🔐 Security and Limitations

- Keep API keys in `.env` and exclude this file from Git.
- Do not upload confidential or restricted college documents to a public repository.
- Scanned PDFs may require OCR because ordinary PDF text extraction may return no text.
- Answers depend on the quality of the source documents and retrieval results.
- The LLM can still generate inaccurate answers; verify important information against the cited PDF pages.
- API usage may incur costs or be subject to provider rate limits.
- The local ChromaDB directory must be generated again if it is not included in the repository.

## 🔮 Future Enhancements

- Upload PDFs directly through Streamlit.
- Support multiple document collections and document selection.
- Add chat history and conversational memory.
- Display retrieved text snippets and similarity scores.
- Improve scanned-document support with OCR.
- Add authentication and administrator access.
- Deploy the frontend and backend for remote access.
- Add document-level filtering and more detailed citations.

## 🎯 Project Objective

The objective of this project is to build an AI-based college information assistant that makes college documents easier to search and understand using semantic retrieval and large language models.

## 👩‍💻 Author

**Ashika S**

AI & Data Science Student

GitHub: [Your GitHub Profile](https://github.com/Ashika3526)

---

⭐ If you find this project useful, consider giving the repository a star.
