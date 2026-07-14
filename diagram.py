from pathlib import Path

diagram = """
flowchart TD

A[User Uploads PDF] --> B[PyPDFLoader]
B --> C[Text Splitter]
C --> D[Gemini Embeddings]
D --> E[Chroma Vector DB]
E --> F[User Question]
F --> G[Retriever]
G --> H[Relevant Chunks]
H --> I[Gemini LLM]
I --> J[Answer]
"""

Path("rag_architecture.mmd").write_text(
    diagram
)

print("Diagram saved")