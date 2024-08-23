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

# Interactive Mode 

Zrb Ollama provides a simple CLI command so you can interact with the LLM immediately. 
To interact with the LLM, you can invoke the following command.

```bash
zrb-ollama
```

To enhance `zrb-ollama` with tools, you can create a file named `zrb_ollama_init.py` and register the tools:

```python
import os
from zrb_ollama import interactive_tools
from zrb_ollama.tools import create_rag, get_rag_documents


_CURRENT_DIR = os.path.dirname(__file__)

retrieve_john_titor_info = create_rag(
    tool_name='retrieve_john_titor_info',
    tool_description="Look for anything related to John Titor",
    documents=get_rag_documents(os.path.join(_CURRENT_DIR, "rag", "document")),
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
    create_rag, get_rag_documents, query_internet
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
            documents=get_rag_documents(os.path.join(_RAG_DIR, "document")),
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
    create_rag, get_rag_documents, query_internet
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
            documents=get_rag_documents(os.path.join(_RAG_DIR, "document")),
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

You can set Zrb Ollama configurations using environment variables.

- `LLM_MODEL`
    - Default: `ollama/mistral:7b-instruct`
    - Description: Default LLM model for `LLMTask` and interactive mode. See [Lite LLM](https://docs.litellm.ai/docs/providers) for valid values.
- `INTERACTIVE_ENABLED_TOOL_NAMES`
    - Default: `query_internet,open_web_page,run_shell_command`
    - Description: Default tools enabled for interactive mode.
- `RAG_EMBEDDING_MODEL`
    - Default: `ollama/nomic-embed-text`
    - Description: Default RAG embedding model for `LLMTask` and interactive mode. See [Lite LLM](https://docs.litellm.ai/docs/providers) for valid values.
- `RAG_CHUNK_SIZE`
    - Default: `1024`
    - Description: Default chunk size for RAG.
- `RAG_OVERLAP`
    - Default: `128`
    - Description: Default chunk overlap size for RAG.
- `RAG_MAX_RESULT_COUNT`
    - Default: `5`
    - Description: Default result count for RAG.
- `DEFAULT_SYSTEM_PROMPT`
    - Default: `You are a helpful assistant.`
    - Description: Default system prompt.
- `DEFAULT_SYSTEM_MESSAGE_TEMPLATE`
    - Default: See [config.py](https://github.com/state-alchemists/zrb-ollama/blob/main/src/zrb_ollama/config.py)
    - Description: Default template for LLM's system message. Should contains the following:
        - `{system_prompt}`
        - `{response_format}`
        - `{function_signatures}`
