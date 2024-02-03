import os

from langchain_openai import OpenAIEmbeddings
from zrb import runner

from zrb_ollama import PromptTask
from zrb_ollama.factory.tool.rag import rag_tool_factory
from zrb_ollama.factory.tool.search import search_tool_factory

CURRENT_DIR = os.path.dirname(__file__)

chat = PromptTask(
    name="chat",
    input_prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    tool_factories=[
        search_tool_factory(),
        rag_tool_factory(
            name="State of the Union Search",
            description="Use this tool to search anything related to the state of the union",  # noqa
            doc_dir_path=os.path.join(CURRENT_DIR, "docs"),
            db_dir_path=os.path.join(CURRENT_DIR, "rag"),
            embeddings=OpenAIEmbeddings(),
        ),
    ],
)
runner.register(chat)
