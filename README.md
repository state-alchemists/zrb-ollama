![](https://raw.githubusercontent.com/goFrendiAsgard/zrb-ollama/main/_images/android-chrome-192x192.png)

# Zrb Ollama

Zrb Ollama is a [Pypi](https://pypi.org) package that acts as LiteLLM's wrapper, allowing you to incorporate LLM into your workflow.

Zrb Ollama is a part of the [Zrb](https://pypi.org/project/zrb) ecosystem, but you can install it independently from Zrb. 

# Installation

You can install Zrb Ollama by invoking any of the following commands:

```bash
# From pypi
pip install zrb-ollama[rag,aws]

# From github
pip install git+https://github.com/state-alchemists/zrb-ollama.git@main

# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

By default, Zrb Ollama uses Ollama-based LLM. You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

The default LLM is `ollama/mistral:7b-instruct`, while the default embedding LLM is `ollama/nomic-embed-text`.

You can change this by setting the `model` parameter on `LLMTask` or the `create_rag` function. See [LiteLLM provider](https://docs.litellm.ai/docs/providers/) to use custom LLM.

# Setup LLM

## Using Ollama

You can intall and use [Ollama](https://ollama.ai) to run models locally. To use Ollama in `zrb-ollama`, you need to set two variables:

- `ZRB_OLLAMA_LLM_MODEL` (set this to `ollama/gemma2`, `ollama/qwen2` or other ollama models)
- `ZRB_OLLAMA_EMBEDDING_MODEL` (set this to `ollama/nomic-embed-text` or other ollama models)

## Using OpenAI

To use OpenAI, you need to set three variables:

- `OPENAI_API_KEY`
- `ZRB_OLLAMA_LLM_MODEL` (set this to `gpt-4o`, `gpt-4o-mini` or other OpenAI models)
- `ZRB_OLLAMA_EMBEDDING_MODEL` (set this to `text-embedding-ada-001` or other OpenAI models)

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

# Create RAG function
retrieve_john_titor_info = create_rag(
    tool_name='retrieve_john_titor_info',
    tool_description="Look for anything related to John Titor",
    documents=get_rag_documents(os.path.join(_CURRENT_DIR, "rag", "document")),
    vector_db_path=os.path.join(_CURRENT_DIR, "rag", "vector"),
    # reset_db=True,
)

# Register RAG function as zrb-ollama tool
interactive_tools.register(retrieve_john_titor_info)


# Create a simple function
def add(a: int, b: int) -> int:
    """Adding two numbers and return the result"""
    return a + b


# Register the function as zrb-ollama tool
interactive_tools.register(add)
```

`zrb-ollama` automatically load `zrb_ollama_init.py` and make any registered tools available in the interface.

## Command

While in interactive mode, you can use the following commands:

```
/?                     Show help
/bye                   Quit
/clear                 Clear context
/multi                 Start multiline mode
/end                   Stop multiline mode
/model [model]         Get/set current model (e.g., ollama/mistral:7b-instruct, gpt-4o)

/tool                  Get list of tools
/tool add <tool-name>  Add tool
/tool rm <tool-name>   Remove tool
```

All commands are started with a `/`.

# Using LLMTask (For Integration with Zrb)

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

# Using Agent (For Integration with Anything Else)

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
    - Default: `You are a helpful assistant. You provide accurate and comprehensive answers.`
    - Description: Default system prompt for LLM Agent.
- `DEFAULT_SYSTEM_MESSAGE_TEMPLATE`
    - Default: See [config.py](https://github.com/state-alchemists/zrb-ollama/blob/main/src/zrb_ollama/config.py)
    - Description: Default template for LLM AGENT's system message. May contains the following:
        - `{system_prompt}`
        - `{response_format}`
        - `{function_signatures}`
- `DEFAULT_JSON_FIXER_SYSTEM_PROMPT`
    - Default: `You are a message fixer. You turn any message into JSON format. Your user is a LLM assistant that need to provide the correctly formatted message to serve the end user (human). If you think the LLM should end the conversation, make sure all necessary information for the human is included in the final_answer.`
    - Description: System prompt to fix main LLM response in case it produces invalid JSON
- `DEFAULT_JSON_FIXER_SYSTEM_MESSAGE_TEMPLATE`
    - Default: See [config.py](https://github.com/state-alchemists/zrb-ollama/blob/main/src/zrb_ollama/config.py)
    - Description: Default system message template to fix main LLM response. May contains the following:
        - `{system_prompt}`
        - `{response_format}`
        - `{function_signatures}`
