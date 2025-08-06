# 🧠 Optimized Input Data Classification & Chunking Strategy

## ✅ Purpose

This strategy classifies and preprocesses input files of different types—text, images, and structured data—for semantic embedding. The goal is to maintain **semantic context** for each format to support **semantic search**, **question answering**, or **retrieval-augmented generation (RAG)**.

---

## 🔍 Step-by-Step Classification Workflow

### 1. Identify File Type

Detect file type by MIME type or extension:

| Format            | Type                  |
|-------------------|------------------------|
| `.txt`, `.md`, `.docx`, `.pdf` | Unstructured text |
| `.jpg`, `.png`, `.gif`         | Image with text    |
| `.csv`, `.json`, `.xml`        | Structured data    |

---

### 2. Select Loader

| File Type        | Loader Name              | Description                             |
|------------------|--------------------------|-----------------------------------------|
| Text             | `UnstructuredFileLoader` | Extracts raw or rich text               |
| Image            | `ImageLoader` + OCR      | OCR via Tesseract or Vision API         |
| Structured Data  | `StructuredDataLoader`   | Parses rows, fields, and metadata       |

---

### 3. Preprocessing Rules

- Remove empty lines and formatting noise
- Normalize whitespace and encoding
- Post-OCR cleanup (for images)

---

## 📦 Chunking Strategy by Data Type

### 📝 A. Text Documents

- **Chunker**: `RecursiveCharacterTextSplitter`
- **chunk_size**: `400–512`
- **chunk_overlap**: `50–100`
- **separators**: `["\n\n", "\n", ".", " ", ""]`
- **Notes**: Preserves semantic units and context flow

---

### 🖼️ B. Images with Text

- **Chunker**: `ImageChunkSplitter` → then text splitter
- **Convert to**: Markdown-like text
- **Post-OCR Chunking**: Use text chunker (as above)
- **Notes**: Preserve table regions and section labels

---

### 📊 C. Structured Data (Tables, CSV, JSON)

- **Chunker**: `StructuredDataChunkSplitter`
- **Strategy**:
  - Chunk row-by-row or 3–5 rows per chunk
  - Convert row to labeled text (e.g., `Field: Value`)
- **Notes**: Ensure field names are present

```text
Product ID: B00813GRG4  
Score: 1  
Review: Not as Advertised  
```

---

## ⚙️ Handling Mixed Content Docs (e.g. `.docx` with text + tables)

1. Use a `SmartDocxParser` to extract both:
    - Paragraphs → `TextChunkSplitter`
    - Tables → `StructuredDataChunkSplitter`

2. Annotate each chunk with metadata:
    ```json
    {
      "type": "text" or "table",
      "source": "docx",
      "section": "Returns Policy"
    }
    ```

3. Normalize to text format before embedding.

---

## 🧠 Semantic Embedding Integration

All content chunks are passed to the embedding model:

```python
from openai import OpenAI

def embed_chunk(text, model="text-embedding-3-small"):
    return client.embeddings.create(input=[text], model=model).data[0].embedding
```

Store in vector DB with metadata (file name, data type, section, etc.)

---

## 📁 Example Output Metadata Format

```json
{
  "embedding": [0.123, -0.456, ...],
  "content": "Product ID: B00813GRG4\nScore: 1\nReview: Not as Advertised...",
  "type": "structured",
  "source_file": "reviews.docx",
  "section": "Table: Product Reviews",
  "chunk_index": 3
}
```

---

## ✅ Summary Table

| Step               | Strategy                                |
|--------------------|-----------------------------------------|
| Detect file type   | Based on extension/MIME                 |
| Load content       | Use specialized loader                  |
| Preprocess         | Normalize + format                      |
| Chunk appropriately| Use per-type strategy                   |
| Embed              | With OpenAI model                       |
| Store metadata     | Chunk type, file name, section, index   |