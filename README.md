# 📚 Docs Q&A Bot

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about PDF and Markdown documents and receive context-based answers with source citations.

The application uses **Qwen2.5 3B through Ollama** for local text generation, **BGE embeddings** for semantic search, and **ChromaDB** for vector storage.

## 🚀 Features

* **Document ingestion:** Load PDF and Markdown files.
* **Text chunking:** Split documents into smaller, overlapping chunks.
* **Semantic search:** Retrieve relevant document chunks using embeddings.
* **Evidence checking:** Apply a lexical evidence gate before generating an answer.
* **Local LLM generation:** Generate answers using Qwen2.5 3B with Ollama.
* **Source citations:** Display document names and page numbers when available.
* **Retrieval evaluation:** Measure retrieval performance using Recall@k.
* **Answer evaluation:** Test answerable and unanswerable questions.
* **Interactive UI:** Ask questions through a Streamlit interface.

## 🏗️ Architecture

```text
PDF / Markdown Documents
          |
          v
   Document Loader
          |
          v
    Text Cleaning
          |
          v
      Chunking
          |
          v
   BGE Embeddings
          |
          v
       ChromaDB
          |
          v
     User Question
          |
          v
  Query Embedding
          |
          v
  Semantic Retrieval
          |
          v
   Evidence Checker
          |
          v
  Qwen2.5 3B (Ollama)
          |
          v
    Generated Answer
          |
          v
   Source Citations
```

**Note:** Text generation runs locally through Ollama. Embeddings currently use Hugging Face Inference, so an internet connection and a Hugging Face token are required for embedding requests.

## 🛠️ Tech Stack

| Component           | Technology               |
| ------------------- | ------------------------ |
| Language            | Python                   |
| LLM                 | Qwen2.5 3B               |
| Inference runtime   | Ollama                   |
| Embedding model     | BAAI/bge-small-en-v1.5   |
| Embedding inference | Hugging Face Inference   |
| Vector database     | ChromaDB                 |
| Chunking            | LangChain Text Splitters |
| PDF processing      | pypdf                    |
| User interface      | Streamlit                |
| Evaluation          | Custom Python scripts    |

## 📂 Project Structure

```text
docs-qa-bot/
│
├── documents/
│   └── sample.md
│
├── evaluation/
│   ├── evaluate_answers.py
│   ├── evaluate_retrieval.py
│   └── inspect_chunks.py
│
├── src/
│   ├── app.py
│   ├── context_builder.py
│   ├── document_loader.py
│   ├── embedding_model.py
│   ├── evidence_checker.py
│   ├── generator.py
│   ├── ingest.py
│   ├── rag.py
│   └── retriever.py
│
├── tests/
│   ├── test_context.py
│   ├── test_loader.py
│   ├── test_rag.py
│   ├── test_real_rag.py
│   └── test_retriever.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The `chroma_db/` directory is generated locally during ingestion and is excluded from Git.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/docs-qa-bot.git
cd docs-qa-bot
```

Replace `YOUR_USERNAME` with the GitHub account that hosts the repository.

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Hugging Face

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token
```

Use a Hugging Face token with the permissions required for inference.

### 5. Install and start Ollama

Install Ollama from [ollama.com](https://ollama.com).

Pull the model:

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before starting the application.

## 📄 Usage

### 1. Add documents

Place PDF and Markdown files inside the `documents/` directory.

PDF files are ignored by Git, so add your own documents locally.

### 2. Ingest documents

From the project root, run:

```bash
python src/ingest.py
```

This loads documents, cleans and chunks the text, generates embeddings, and stores them in ChromaDB.

Run ingestion again when the documents in your knowledge base change.

### 3. Launch the application

```bash
streamlit run src/app.py
```

Open the local URL displayed in your terminal.

Enter a question about your documents and review the generated answer and its sources.

## 📊 Evaluation

The project includes separate scripts for evaluating retrieval and answer generation.

### Retrieval evaluation

```bash
python evaluation/evaluate_retrieval.py
```

Latest recorded results:

| Metric   |       Result |
| -------- | -----------: |
| Recall@1 |   50% (5/10) |
| Recall@3 | 100% (10/10) |

These results are from a 10-question answerable retrieval evaluation set. Recall@3 of 100% means the expected relevant chunk was retrieved within the top three results for all 10 questions. It does not represent overall answer accuracy.

### Answer evaluation

```bash
python evaluation/evaluate_answers.py
```

Latest recorded results:

* 4 out of 4 answerable questions answered correctly.
* 3 out of 3 unanswerable questions rejected.

These are results from a small evaluation set and should not be interpreted as a general performance guarantee.

## 🧠 Key Design Decisions

* **Top-3 retrieval:** Retrieve multiple chunks to provide the generator with sufficient context.
* **Evidence checker:** Use a deterministic lexical overlap check to reject questions that appear unsupported by retrieved context.
* **Local generation:** Use Ollama and Qwen2.5 3B instead of an external LLM generation API.
* **Deterministic citations:** Generate source references in Python using retrieval metadata rather than relying on the LLM to produce citations.
* **Separate evaluation:** Evaluate retrieval and answer generation independently to make system behavior easier to inspect.

## 🔮 Future Improvements

* Improve retrieval ranking and Recall@1.
* Explore reranking models.
* Improve evidence checking beyond lexical overlap.
* Add document upload and knowledge-base management through the UI.
* Expand evaluation with larger and more diverse datasets.
* Explore fully local embeddings for offline operation.
