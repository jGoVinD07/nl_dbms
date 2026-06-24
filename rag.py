import chromadb
from build_rag import OllamaEmbeddingFunction

client = chromadb.PersistentClient(path="./rag_db")

ef = OllamaEmbeddingFunction()

collection = client.get_collection("schema", embedding_function=ef)




def retrieve_context(question):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    docs = results["documents"][0]

    return "\n".join(docs)


def table_exists(table_name):

    try:

        data = collection.get(
            ids=[table_name.lower()]
        )

        return len(data["ids"]) > 0

    except:

        return False


def get_all_tables():

    try:

        data = collection.get()

        return data["ids"]

    except:

        return []