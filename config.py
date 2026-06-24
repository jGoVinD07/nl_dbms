# Central configuration — change model names, DB credentials, and paths here

# Database
DB_HOST = "localhost"
DB_NAME = "school"
DB_USER = "postgres"
DB_PASSWORD = "abcd"

# Embedding model (Ollama)
EMBEDDING_MODEL = "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf:latest"

# LLM model (Ollama)
LLM_MODEL = "llama3.1:latest"

# ChromaDB
CHROMA_PATH = "./rag_db"
CHROMA_COLLECTION = "schema"
