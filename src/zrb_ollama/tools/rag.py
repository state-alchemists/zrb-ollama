from typing import Callable
import litellm
import json
import os


def create_rag(
    document: str,
    rag_description: str,
    rag_name: str = "retrieve",
    model: str = "ollama/nomic-embed-text",
    vector_db_path: str = "./chroma",
    vector_db_collection: str = "documents",
    reset_db: bool = True,
    chunk_size: int = 512,
    overlap: int = 128,
    max_result_count: int = 5,
) -> Callable[[str], str]:
    import chromadb
    from chromadb.config import Settings

    def retrieve(query: str) -> str:
        client = chromadb.PersistentClient(
            path=vector_db_path,
            settings=Settings(allow_reset=True)
        )
        if not os.path.isdir(vector_db_path) or reset_db:
            client.reset()
            collection = client.get_or_create_collection(vector_db_collection)
            chunks = []
            for i in range(0, len(document), chunk_size - overlap):
                chunk = document[i:i + chunk_size]
                if len(chunk) > 0:
                    chunks.append(chunk)
            # Generate embeddings and save to ChromaDB
            ids = []
            embeddings = []
            documents = []
            for index, chunk in enumerate(chunks):
                response = litellm.embedding(
                    model='text-embedding-ada-002', input=[chunk]
                )
                ids.append(f"id{index}")
                embeddings.append(response["data"][0]["embedding"])
                documents.append(chunk)
            collection.upsert(ids=ids, documents=documents, embeddings=embeddings)
        # Generate embedding for the query
        response = litellm.embedding(model=model, input=[query])
        collection = client.get_or_create_collection(vector_db_collection)
        # Search for the top_k most similar documents
        results = collection.query(
            query_embeddings=response["data"][0]["embedding"],
            n_results=max_result_count
        )
        return json.dumps(results)
    retrieve.__name__ = rag_name
    retrieve.__doc__ = rag_description
    return retrieve
