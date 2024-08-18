import json
import os
from collections.abc import Callable, Iterable

import litellm
import pdfplumber
from zrb.helper.accessories.color import colored
from zrb.helper.callable import run_async

from ..config import (
    RAG_CHUNK_SIZE,
    RAG_EMBEDDING_MODEL,
    RAG_MAX_RESULT_COUNT,
    RAG_OVERLAP,
)


def create_rag(
    tool_name: str,
    tool_description: str,
    documents: Iterable[str | Callable[[], str]] = [],
    model: str = RAG_EMBEDDING_MODEL,
    vector_db_path: str = "./chroma",
    vector_db_collection: str = "documents",
    reset_db: bool = False,
    chunk_size: int = RAG_CHUNK_SIZE,
    overlap: int = RAG_OVERLAP,
    max_result_count: int = RAG_MAX_RESULT_COUNT,
) -> Callable[[str], str]:
    import chromadb
    from chromadb.config import Settings

    async def retrieve(query: str) -> str:
        is_db_exist = os.path.isdir(vector_db_path)
        client = chromadb.PersistentClient(
            path=vector_db_path, settings=Settings(allow_reset=True)
        )
        if not is_db_exist or reset_db:
            client.reset()
            collection = client.get_or_create_collection(vector_db_collection)
            chunk_index = 0
            _print_dark("Scanning documents")
            for document in documents:
                if callable(document):
                    document = await run_async(document)
                for i in range(0, len(document), chunk_size - overlap):
                    chunk = document[i : i + chunk_size]
                    if len(chunk) > 0:
                        _print_dark(f"Vectorizing chunk {chunk_index}")
                        response = await litellm.aembedding(model=model, input=[chunk])
                        vector = response["data"][0]["embedding"]
                        _print_dark(f"Adding chunk {chunk_index} to db")
                        collection.upsert(
                            ids=[f"id{chunk_index}"],
                            embeddings=[vector],
                            documents=[chunk]
                        )
                        chunk_index += 1
        collection = client.get_or_create_collection(vector_db_collection)
        # Generate embedding for the query
        _print_dark("Vectorize query")
        query_response = await litellm.aembedding(model=model, input=[query])
        _print_dark("Search documents")
        # Search for the top_k most similar documents
        results = collection.query(
            query_embeddings=query_response["data"][0]["embedding"],
            n_results=max_result_count,
        )
        return json.dumps(results)

    retrieve.__name__ = tool_name
    retrieve.__doc__ = tool_description
    return retrieve


def documents_from_directory(directory: str) -> list[Callable[[], str]]:
    # Walk through the directory
    readers = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(".pdf"):
                readers.append(get_pdf_reader(file_path))
                continue
            readers.append(get_text_reader(file_path))
    return readers


def get_text_reader(file_path: str):
    def read():
        _print_dark(f"Start reading {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        _print_dark(f"Complete reading {file_path}")
        return content

    return read


def get_pdf_reader(file_path):
    def read():
        _print_dark(f"Start reading {file_path}")
        contents = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                contents.append(page.extract_text())
        _print_dark(f"Complete reading {file_path}")
        return "\n".join(contents)

    return read


def _print_dark(text: str):
    print(colored(f"{text}", attrs=["dark"]))
