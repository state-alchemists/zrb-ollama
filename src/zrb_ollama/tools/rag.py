from typing import Callable, Iterable
from zrb.helper.accessories.color import colored
from zrb.helper.callable import run_async
import litellm
import json
import os


def create_rag(
    rag_description: str,
    documents: Iterable[str | Callable[[], str]] = [],
    rag_name: str = "retrieve",
    model: str = "ollama/nomic-embed-text",
    vector_db_path: str = "./chroma",
    vector_db_collection: str = "documents",
    reset_db: bool = False,
    chunk_size: int = 512,
    overlap: int = 128,
    max_result_count: int = 5,
) -> Callable[[str], str]:
    import chromadb
    from chromadb.config import Settings

    async def retrieve(query: str) -> str:
        is_db_exist = os.path.isdir(vector_db_path)
        client = chromadb.PersistentClient(
            path=vector_db_path,
            settings=Settings(allow_reset=True)
        )
        if not is_db_exist or reset_db:
            chunks = []
            _print_dark("Load documents")
            for document in documents:
                if callable(document):
                    document = await run_async(document)
                for i in range(0, len(document), chunk_size - overlap):
                    chunk = document[i:i + chunk_size]
                    if len(chunk) > 0:
                        chunks.append(chunk)
            # Generate embeddings and save to ChromaDB
            vector_ids = []
            vector_embeddings = []
            vector_documents = []
            _print_dark("Vectorize documents")
            for index, chunk in enumerate(chunks):
                response = await litellm.aembedding(model=model, input=[chunk])
                vector_ids.append(f"id{index}")
                vector_embeddings.append(response["data"][0]["embedding"])
                vector_documents.append(chunk)
            # Create collection and upsert
            _print_dark("Save vectors")
            client.reset()
            collection = client.get_or_create_collection(vector_db_collection)
            collection.upsert(
                ids=vector_ids, documents=vector_documents, embeddings=vector_embeddings
            )
        # Generate embedding for the query
        _print_dark("Vectorize query")
        query_response = await litellm.aembedding(model=model, input=[query])
        _print_dark("Search documents")
        collection = client.get_or_create_collection(vector_db_collection)
        # Search for the top_k most similar documents
        results = collection.query(
            query_embeddings=query_response["data"][0]["embedding"],
            n_results=max_result_count
        )
        return json.dumps(results)
    retrieve.__name__ = rag_name
    retrieve.__doc__ = rag_description
    return retrieve


def _print_dark(text: str):
    print(colored(f"{text}", attrs=["dark"]))
