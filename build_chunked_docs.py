import os
import json
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Directory containing onboarding documents
docs_dir = 'onboarding-docs'
output_file = 'chunked_docs.json'

# Supported file extensions and their loaders
loaders = {
    '.pdf': PyPDFLoader,
    '.docx': Docx2txtLoader,
    '.md': UnstructuredFileLoader,
    '.txt': UnstructuredFileLoader,
    '.html': UnstructuredFileLoader,
}

# Chunking parameters
chunk_size = 500
chunk_overlap = 100
separators = ["\n\n", "\n", ".", " "]

all_chunks = []

for fname in os.listdir(docs_dir):
    fpath = os.path.join(docs_dir, fname)
    ext = os.path.splitext(fname)[1].lower()
    if ext not in loaders:
        continue
    loader = loaders[ext](fpath)
    try:
        docs = loader.load()
    except Exception as e:
        print(f"Failed to load {fname}: {e}")
        continue
    # Filter out empty pages/sections
    docs = [d for d in docs if d.page_content.strip()]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    for doc in docs:
        # Split into chunks
        chunks = splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            # Extract role, stage from filename if possible
            # Example: QA_Week1_Intro.docx -> role=QA, stage=Week1
            parts = fname.split('_')
            role = parts[0] if len(parts) > 0 else ''
            stage = parts[1] if len(parts) > 1 else ''
            metadata = {
                'role': role,
                'stage': stage,
                'source': fname,
                'page': getattr(doc.metadata, 'page', None)
            }
            all_chunks.append({
                'text': chunk,
                'metadata': metadata
            })

# Save to JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print(f"Exported {len(all_chunks)} chunks to {output_file}")
