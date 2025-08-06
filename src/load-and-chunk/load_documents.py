import os
import json
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredFileLoader

def load_documents(input_path):
    """
    Load documents from a directory or a specific file and return a list of document objects (no chunking).
    """
    loaders = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.md': UnstructuredFileLoader,
        '.txt': UnstructuredFileLoader,
        '.html': UnstructuredFileLoader,
    }
    all_docs = []

    def process_file(fpath, fname):
        ext = os.path.splitext(fname)[1].lower()
        if ext not in loaders:
            return
        loader = loaders[ext](fpath)
        try:
            docs = loader.load()
        except Exception as e:
            print(f"Failed to load {fname}: {e}")
            return
        docs = [d for d in docs if d.page_content.strip()]
        for doc in docs:
            parts = fname.split('_')
            role = parts[0] if len(parts) > 0 else ''
            stage = parts[1] if len(parts) > 1 else ''
            metadata = {
                'role': role,
                'stage': stage,
                'source': fname,
                'page': getattr(doc.metadata, 'page', None)
            }
            all_docs.append({
                'text': doc.page_content,
                'metadata': metadata
            })

    if os.path.isdir(input_path):
        for fname in os.listdir(input_path):
            fpath = os.path.join(input_path, fname)
            if os.path.isfile(fpath):
                process_file(fpath, fname)
    elif os.path.isfile(input_path):
        process_file(input_path, os.path.basename(input_path))
    else:
        raise ValueError("Input path is not a valid file or directory.")

    return all_docs

# Example usage:
if __name__ == "__main__":
    docs_dir = 'docs/onboarding-docs'
    documents = load_documents(docs_dir)
    with open('docs/data-warehouse/loaded_docs.json', 'w') as f:
        json.dump(documents, f, indent=2)
    print(f"Loaded {len(documents)} documents.")
