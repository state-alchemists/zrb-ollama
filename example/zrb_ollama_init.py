import os
from zrb_ollama import interactive_tools
from zrb_ollama.tools import create_rag, documents_from_directory


_CURRENT_DIR = os.path.dirname(__file__)

retrieve_john_titor_info = create_rag(
    tool_name='retrieve_john_titor_info',
    tool_description="Look for anything related to John Titor",
    documents=documents_from_directory(os.path.join(_CURRENT_DIR, "rag", "document")),
    vector_db_path=os.path.join(_CURRENT_DIR, "rag", "vector"),
    # reset_db=True,
)
interactive_tools.register(retrieve_john_titor_info)
