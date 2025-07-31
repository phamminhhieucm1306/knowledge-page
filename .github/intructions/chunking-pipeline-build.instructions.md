# Phase 1 – Document Reader & Chunker (Python + LangChain)

## 🛠️ Setup
- [ ] Create a Python virtual environment and install required packages:
  - langchain
  - pypdf
  - docx2txt
  - unstructured
  - tiktoken

## 📁 Document Ingestion
- [ ] Read all files from the `onboarding-docs/` directory
- [ ] Use the correct loader based on file extension:
  - `.pdf` → `PyPDFLoader`
  - `.docx` → `Docx2txtLoader`
  - `.md`, `.txt`, `.html` → `UnstructuredFileLoader`

## 📄 Preprocessing
- [ ] Normalize file encoding and extract text cleanly
- [ ] Filter out empty pages or irrelevant sections (e.g., cover pages)

## ✂️ Chunking Strategy
- [ ] Use `RecursiveCharacterTextSplitter` with the following parameters:
  - chunk_size: 500
  - chunk_overlap: 100
  - separators: `["\n\n", "\n", ".", " "]`
- [ ] Split each document into meaningful LLM-friendly chunks

## 🏷️ Metadata Enrichment
- [ ] Add metadata to each chunk:
  - role: e.g., `QA`, `DEV`, `SM`, `BA`
  - stage: e.g., `Week1`, `Sprint2`
  - source: file name
  - page: page number (if available)

## 💾 Save Output
- [ ] Convert the list of chunks to a dictionary:
  - `text`
  - `metadata`
- [ ] Export all chunks as a JSON file: `chunked_docs.json`

## 🧪 Optional Testing
- [ ] Add a CLI command to preview a random chunk and its metadata
- [ ] Validate output structure before embedding
