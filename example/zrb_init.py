from zrb import runner, StrInput
from zrb_ollama import LLMTask
from zrb_ollama.tools import query_internet, create_rag

import os

_CURRENT_DIR = os.path.dirname(__file__)
with open(os.path.join(_CURRENT_DIR, "john-titor.md")) as f:
    john_titor_article = f.read()

ask = LLMTask(
    name="ask",
    inputs=[
        StrInput(name="user-prompt", default="How John Titor introduce himself?"),
    ],
    model="gpt-4o",
    user_message="{{input.user_prompt}}",
    tools=[
        create_rag(
            document=john_titor_article,
            model="text-embedding-ada-002",
            rag_description="Look for anything related to John Titor"
        ),
        query_internet,
    ]
)
runner.register(ask)
