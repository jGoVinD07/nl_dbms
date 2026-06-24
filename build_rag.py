import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
import ollama
from db import get_connection


class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf:latest"):
        self.model = model

    def __call__(self, input):
        return [
            ollama.embeddings(model=self.model, prompt=text)["embedding"]
            for text in input
        ]


client = chromadb.PersistentClient(path="./rag_db")

collection = client.get_or_create_collection(
    "schema",
    embedding_function=OllamaEmbeddingFunction()
)


def build_rag():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    """)

    tables = cursor.fetchall()

    existing_ids = set(
        collection.get()["ids"]
    )

    current_ids = set()

    for table in tables:

        table_name = table[0]

        current_ids.add(
            table_name
        )

        cursor.execute("""
        SELECT column_name,data_type
        FROM information_schema.columns
        WHERE table_name=%s
        ORDER BY ordinal_position
        """, (table_name,))

        columns = cursor.fetchall()

        doc = f"""
Table: {table_name}

Columns:
"""

        for col in columns:

            doc += f"""
{col[0]} ({col[1]})
"""

        collection.upsert(
            ids=[table_name],
            documents=[doc]
        )

    # Remove deleted tables from RAG

    removed_tables = existing_ids - current_ids

    if removed_tables:

        collection.delete(
            ids=list(removed_tables)
        )

    cursor.close()
    conn.close()


if __name__ == "__main__":

    build_rag()

    print("RAG Built")