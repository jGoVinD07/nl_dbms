import chromadb
from config import CHROMA_PATH, CHROMA_COLLECTION
from rag.embeddings import OllamaEmbeddingFunction

def _get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        CHROMA_COLLECTION,
        embedding_function=OllamaEmbeddingFunction()
    )

_collection = _get_collection()


def retrieve_context(question, n_results=3):
    results = _collection.query(
        query_texts=[question],
        n_results=n_results
    )
    return "\n".join(results["documents"][0])


def table_exists(table_name):
    try:
        data = _collection.get(ids=[table_name.lower()])
        return len(data["ids"]) > 0
    except:
        return False


def get_all_tables():
    try:
        return _collection.get()["ids"]
    except:
        return []
