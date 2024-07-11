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

# Using LLMTask

Zrb Ollama provides a task named `LLMTask`, allowing you to create a Zrb Task with a custom model or tools.

```python
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
            documents=[john_titor_article],
            model="text-embedding-ada-002",
            rag_description="Look for anything related to John Titor"
        ),
        query_internet,
    ]
)
runner.register(ask)
```

Assuming there is a file named `john-titor.md`, you can invoke the Task by invoking the following command.

```bash
zrb ask
```

The LLM can browse the article or look for anything on the internet.

# Using Agent

Under the hood, LLMTask makes use of Agent. You can create and interact with the agent programmatically as follows.

```python
from zrb_ollama import agent
from zrb_ollama.tools import create_rag, query_internet

import asyncio
import os

_CURRENT_DIR = os.path.dirname(__file__)
with open(os.path.join(_CURRENT_DIR, "john-titor.md")) as f:
    john_titor_article = f.read()


agent = Agent(
    model="gpt-4o",
    tools=[
        create_rag(
            documents=[john_titor_article],
            model="text-embedding-ada-002",
            rag_description="Look for anything related to John Titor"
        ),
        query_internet,
    ]
)
result = asyncio.run(agent.add_user_message("How John Titor introduce himself?"))
print(result)
```


