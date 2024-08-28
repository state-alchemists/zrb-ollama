import os
from zrb_ollama import interactive_tools
from zrb_ollama.tools import create_rag_from_directory


_CURRENT_DIR = os.path.dirname(__file__)


retrieve_john_titor_info = create_rag_from_directory(
    tool_name='retrieve_john_titor_info',
    tool_description="Look for anything related to John Titor",
    # model="text-embedding-ada-002",
    document_dir_path=os.path.join(_CURRENT_DIR, "rag", "document"),
    vector_db_path=os.path.join(_CURRENT_DIR, "rag", "vector"),
)
interactive_tools.register(retrieve_john_titor_info)
