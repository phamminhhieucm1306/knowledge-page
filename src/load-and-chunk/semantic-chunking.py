'''
Concept
------
Instead of arbitrarily slicing text by length, semantic chunking splits documents at logical boundaries (e.g., sentences, paragraphs, or sections).
Often, consecutive segments that are highly similar may be merged, providing coherent text blocks.
'''

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import re
import json
# Ensure the project root is in sys.path for module resolution
from load_documents import load_documents

# Description for the function
def perform_semantic_chunking(document, chunk_size=500, chunk_overlap=100, doc_metadata=None):
    """
    Performs semantic chunking on a document using recursive character splitting 
    at logical text boundaries.
    
    Args:
        document (str): The text document to process
        chunk_size (int): The target size of each chunk in characters
        chunk_overlap (int): The number of characters of overlap between chunks
        
    Returns:
        list: The semantically chunked documents with metadata
    """
    
    # Create the text splitter with semantic separators
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    # Split the text into semantic chunks
    semantic_chunks = text_splitter.split_text(document)
    print(f"Document split into {len(semantic_chunks)} semantic chunks")
    
    # Determine section titles for enhanced metadata
    section_patterns = [
        r'^#+\s+(.+)$',      # Markdown headers
        r'^.+\n[=\-]{2,}$',  # Underlined headers
        r'^[A-Z\s]+:$'       # ALL CAPS section titles
    ]
    
    # Convert to Document objects with enhanced metadata
    documents = []
    current_section = "Introduction"
    
    for i, chunk in enumerate(semantic_chunks):
        # Try to identify section title from chunk
        chunk_lines = chunk.split('\n')
        for line in chunk_lines:
            for pattern in section_patterns:
                match = re.match(pattern, line, re.MULTILINE)
                if match:
                    current_section = match.group(0)
                    break
        
        # Calculate semantic density (ratio of non-stopwords to total words)
        words = re.findall(r'\b\w+\b', chunk.lower())
        stopwords = ['the', 'and', 'is', 'of', 'to', 'a', 'in', 'that', 'it', 'with', 'as', 'for']
        content_words = [w for w in words if w not in stopwords]
        semantic_density = len(content_words) / max(1, len(words))
        
        # Use doc_metadata for role, stage, source
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk_id": i,
                "total_chunks": len(semantic_chunks),
                "chunk_size": len(chunk),
                "chunk_type": "semantic",
                "section": current_section,
                "role": doc_metadata.get("role", "") if doc_metadata else "",
                "stage": doc_metadata.get("stage", "") if doc_metadata else "",
                "source": doc_metadata.get("source", "") if doc_metadata else "",
                "semantic_density": round(semantic_density, 2)
            }
        )
        documents.append(doc)
    
    return documents


# Example usage
if __name__ == "__main__":
    docs = load_documents('docs/onboarding-docs')
    if not docs:
        print("No documents loaded.")
    else:
        all_chunked_docs = []
        for doc in docs:
            chunked_docs = perform_semantic_chunking(doc['text'], doc_metadata=doc['metadata'])
            for d in chunked_docs:
                all_chunked_docs.append({
                    "page_content": d.page_content,
                    "metadata": d.metadata
                })
        with open('docs/data-warehouse/chunked_docs.json', 'w') as f:
            json.dump(all_chunked_docs, f, indent=2)
        print(f"Stored {len(all_chunked_docs)} chunked documents from {len(docs)} source documents.")