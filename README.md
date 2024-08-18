![](https://raw.githubusercontent.com/goFrendiAsgard/zrb-ollama/main/_images/android-chrome-192x192.png)

# Zrb Ollama

Zrb Ollama is a [Pypi](https://pypi.org) package that acts as LiteLLM's wrapper, allowing you to incorporate LLM into your workflow.

Zrb Ollama is a part of the [Zrb](https://pypi.org/project/zrb) ecosystem, but you can install it independently from Zrb. 

# Installation

You can install Zrb Ollama by invoking any of the following commands:

```bash
# From pypi
pip install zrb-ollama[chromadb,aws]

# From github
pip install git+https://github.com/state-alchemists/zrb-ollama.git@main

# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

By default, Zrb Ollama uses Ollama-based LLM. You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

The default LLM is `ollama/mistral:7b-instruct`, while the default embedding LLM is `ollama/nomic-embed-text`.

You can change this by setting the `model` parameter on `LLMTask` or the `create_rag` function. See [LiteLLM provider](https://docs.litellm.ai/docs/providers/) to use custom LLM.

# CLI Command 

Zrb Ollama provides a simple CLI command so you can interact with the LLM immediately. The LLM has two tools:

- query_internet
- run_shell_command

To interact with the LLM, you can invoke the following command.

```bash
zrb-ollama
```

To enhance `zrb-ollama` with tools, you can create a file named `zrb_ollama_init.py` and register the tools:

```python
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
```


# Using LLMTask

Zrb Ollama provides a task named `LLMTask`, allowing you to create a Zrb Task with a custom model or tools.

```python
import os

from zrb import CmdTask, StrInput, runner
from zrb_ollama import LLMTask, ToolFactory
from zrb_ollama.tools import (
    create_rag, documents_from_directory, query_internet
)

_CURRENT_DIR = os.path.dirname(__file__)
_RAG_DIR = os.path.join(_CURRENT_DIR, "rag")

rag = LLMTask(
    name="rag",
    inputs=[
        StrInput(name="user-prompt", default="How John Titor introduce himself?"),
    ],
    # model="gpt-4o",
    user_message="{{input.user_prompt}}",
    tools=[query_internet],
    tool_factories=[
        ToolFactory(
            create_rag,
            tool_name="retrieve_john_titor_info",
            tool_description="Look for anything related to John Titor",
            documents=documents_from_directory(os.path.join(_RAG_DIR, "document")),
            # model="text-embedding-ada-002",
            vector_db_path=os.path.join(_RAG_DIR, "vector"),
            # reset_db=True,
        )
    ],
)
runner.register(rag)
```

Assuming there is a file named `john-titor.md` inside `rag/documents` folder, you can invoke the Task by invoking the following command.

```bash
zrb rag
```

The LLM can browse the article or look for anything on the internet.

# Using Agent

Under the hood, LLMTask makes use of Agent. You can create and interact with the agent programmatically as follows.

```python
import asyncio
import os

from zrb import CmdTask, StrInput, runner
from zrb_ollama import agent
from zrb_ollama.tools import (
    create_rag, documents_from_directory, query_internet
)

_CURRENT_DIR = os.path.dirname(__file__)
_RAG_DIR = os.path.join(_CURRENT_DIR, "rag")


from zrb_ollama.tools import create_rag, query_internet


agent = Agent(
    model="gpt-4o",
    tools=[
        create_rag(
            tool_name="retrieve",
            tool_description="Look for anything related to John Titor"
            documents=documents_from_directory(os.path.join(_RAG_DIR, "document")),
            # model="text-embedding-ada-002",
            vector_db_path=os.path.join(_RAG_DIR, "vector"),
            # reset_db=True,
        ),
        query_internet,
    ]
)
result = asyncio.run(agent.add_user_message("How John Titor introduce himself?"))
print(result)
```

# Configurations

- `LLM_MODEL`
    - default: `ollama/mistral:7b-instruct`
- `INTERACTIVE_ENABLED_TOOL_NAMES`
    - default: `query_internet,open_web_page,run_shell_command`
- `RAG_EMBEDDING_MODEL`
    - default: `ollama/nomic-embed-text`
- `RAG_CHUNK_SIZE`
    - default: `1024`
- `RAG_OVERLAP`
    - default: `128`
- `RAG_MAX_RESULT_COUNT`
    - default: `5`
- `DEFAULT_SYSTEM_PROMPT`
    - default: `You are a helpful assistant.`
- `DEFAULT_SYSTEM_MESSAGE_TEMPLATE`
    - default: See 
