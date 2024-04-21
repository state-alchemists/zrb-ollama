import os
import sys
import importlib.util
from typing import List, Callable
from langchain_core.embeddings import Embeddings

from zrb.helper.util import to_human_readable
from zrb.helper.accessories.color import colored

from ..schema import ToolFactory
from ...config import DOCUMENT_DIRS, EMBEDDING_DB_DIR


def default_tool_factories() -> List[ToolFactory]:
    from .bash_repl import bash_repl_tool_factory
    from .python_repl import python_repl_tool_factory
    from .search import search_tool_factory

    document_dirs = [doc_dir for doc_dir in DOCUMENT_DIRS.split(":") if doc_dir != ""]
    rag_tool_factories = _create_rag_tool_factories(document_dirs)
    factories: List[ToolFactory] = [
        *rag_tool_factories,
        search_tool_factory(),
        bash_repl_tool_factory(),
        python_repl_tool_factory(),
    ]
    return factories


def _create_rag_tool_factories(document_dirs: List[str]) -> List[ToolFactory]:
    if len(document_dirs) == 0:
        return []
    if 'faiss' not in sys.modules:
        spec = importlib.util.find_spec('faiss')
        if spec is None:
            print(
                colored("Faiss is required for document embedding", color="red"),
                file=sys.stderr
            )
            return []
    from ...embedding.helper import get_default_rag_embedding
    from .rag import rag_tool_factory
    embeddings = get_default_rag_embedding()
    return [
        _create_rag_tool_factory(
            rag_tool_factory, document_dir, embeddings
        )
        for document_dir in DOCUMENT_DIRS.split(":") if document_dir != ""
    ]


def _create_rag_tool_factory(
    rag_tool_factory: Callable[..., ToolFactory],
    document_dir: str,
    embeddings: Embeddings
) -> ToolFactory:
    dir_base_name = os.path.basename(document_dir)
    human_dir_base_name = to_human_readable(dir_base_name).capitalize()
    return rag_tool_factory(
        name=f"{human_dir_base_name} Search",
        description=f"Use this tool to search for {human_dir_base_name} documents.",
        doc_dir_path=document_dir,
        db_dir_path=os.path.join(EMBEDDING_DB_DIR, dir_base_name),
        embeddings=embeddings
    )
