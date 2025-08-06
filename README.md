# knowledge_page

A knowledge base management tool for onboarding and documentation.

## Project Structure

```
knowledge-page/
├── src/
│   └── knowledge_page/
│       ├── __init__.py
│       ├── module1.py
│       ├── module2.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_module2.py
├── docs/
│   └── index.md
├── requirements.txt
├── pyproject.toml
├── setup.py
├── README.md
├── .gitignore
└── main.py
```

## Setup

1. **Create a virtual environment and activate it:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```


## Usage

- Place your source code in `src/knowledge_page/`.
- Add tests in `tests/`.
- Documentation goes in `docs/`.
- The main entry point for running the app is `main.py`:
  ```powershell
  python main.py
  ```
  This will print a welcome message and can be extended to run your application logic.

## How the Workflow Works

1. **Document Ingestion:**
   - Place your onboarding documents (`.pdf`, `.docx`, `.md`, `.txt`, `.html`) in the `onboarding-docs/` directory.

2. **Chunking Pipeline:**
   - Run the script to process and chunk the documents:
     ```powershell
     python build_chunked_docs.py
     ```
   - The script will:
     - Load each document using the appropriate loader.
     - Normalize and clean the text.
     - Filter out empty or irrelevant sections.
     - Split the text into LLM-friendly chunks (500 tokens, 100 overlap).
     - Enrich each chunk with metadata (role, stage, source, page).
     - Export all chunks to `chunked_docs.json`.

3. **Output:**
   - The output file `chunked_docs.json` contains a list of chunks, each with its text and metadata.

## Example Output Structure

```json
[
  {
    "text": "...chunk text...",
    "metadata": {
      "role": "QA",
      "stage": "Week1",
      "source": "QA_Week1_Intro.docx",
      "page": 1
    }
  },
  ...
]
```