![](https://raw.githubusercontent.com/goFrendiAsgard/zrb-ollama/main/_images/android-chrome-192x192.png)

# Zrb Ollama

Zrb Ollama is a [pypi](https://pypi.org) package that acts as Ollama's and LangChain's wrapper, allowing you to incorporate LLM into your workflow.

Zrb Ollama is a part of [Zrb](https://pypi.org/project/zrb) ecosystem, but you can install it independently from Zrb. 

# Installation

You can install Zrb Ollama by invoking any of the following commands:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/state-alchemists/zrb-ollama.git@main
# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

By default, Zrb Ollama uses Ollama-based LLM. You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

You can, however, change this behavior by setting `ZRB_LLM_PROVIDER` into `openai` or `bedrock`.

# Configuration

You can configure Zrb Ollama using a few environment variables.

## General Configuration

- `ZRB_LLM_PROVIDER`: LLM Provider (i.e., `ollama`, `openai`, `bedrock`). If not specified, Zrb Ollama will use `ollama`
- `ZRB_SYSTEM_PROMPT` Default system prompt
- `ZRB_CHAT_HISTORY_RETENTION`: Default: 3
- `ZRB_EMBEDDING_DB_DIR`: Directory to store document embedding. By default, it is `~/.zrb-embedding`.
- `ZRB_CHAT_HISTORY_FILE`: File to store past conversations. By default, it is `~/.zrb-ollama-history.txt`)
- `ZRB_DOCUMENT_DIRS`: List of directories for RAG, separated by `:`.

## Ollama Configuration

- `ZRB_OLLAMA_BASE_URL`: Default Ollama base URL. If not specified, Zrb Ollama will use `http://localhost:11434`.
- `ZRB_OLLAMA_MODEL`: Default Ollama model. If not specified, Zrb Ollama will use `mistral:latest`.
- `ZRB_OLLAMA_MODEL`: Default Ollama embedding model (Used for RAG). If not specified, Zrb Ollama will use `mistral:latest`.

## Open AI Configuration

- `OPENAI_API_KEY`: OpenAI API key
- `OPENAI_MODEL`: OpenAI model (Default to `gpt-3.5-turbo-instruct`)
- `OPENAI_API_BASE`: OpenAI base URL, default to empty.

## AWS Configuration

- `AWS_ACCESS_KEY`: AWS Access Key
- `AWS_SECRET_ACCESS_KEY`: AWS Secret Key
- `AWS_REGION_NAME`: AWS Region (By default, it is `us-east-1`)
- `BEDROCK_MODEL_ID`: Default bedrock model (By default, it is `anthropic.claude-v2`)

# Talk to Zrb Ollama

You can effortlessly enjoy RAG functionality.

```bash
export OPENAI_API_KEY=your-api-key
export ZRB_LLM_PROVIDER=openai
export ZRB_DOCUMENT_DIRS=${HOME}/borg/src/daily/notes
zrb-ollama
```

Let's see some conversation recaps.

## Who are you?

The AI can answer this question without using any tool.

```
Human: Who are you?

Assistant: I am Assistant, a large language model designed to assist humans in a wide variety of tasks. I am always here to help you with any questions or tasks you may have.
```

## What are you capable of?

Again, the AI can answer this question without using any tool.

```
Human: What are you capable of?

Assistant: I am capable of assisting you in a wide variety of tasks, such as searching for information, executing bash or python scripts, and providing you with notes. Is there something specific you would like me to help you with?
```

## What did I write in my notes?

Now, the AI needs to use an `RAG tool`. It will parse your `ZRB_DOCUMENT_DIRS`, turn that into a vector database, and answer the question for you.

```
Human: What did I write in my notes?

Assistant: You wrote about your experience with a text expander and how it has increased your productivity. You also mentioned using Zrb to define flows and the possibility of using a simple abbreviation for Zrb commands. Additionally, you discussed exploring the click framework and the current issues with Zrb commands, such as being slow and verbose.
```

## Show me the content of my notes!

To answer this question, the AI needs to use `Bash REPL`.

```
Human: I wrote my notes in /home/gofrendi/borg/src/daily/notes/ directory. The notes were written in markdown format (*.md). Show me the content of my notes as is.
Assistant: Here is the content of your notes in markdown format:

# Text expander

- It seems to be simple but highly increase productivity
- Zrb has handle this in some way, and I'm happy with how I can define flows with zrb (despite of the performance problem on my samsung A4 tablet).
- Probably what I need to provide is a simple abreviation for Zrb commands. It is painful already, since I already create a shell function named "ztadd", which is alias to "zrb todo add -t $*"
- Probably I should explore click framework. The problem with zrb commands are currently:
   - Slow (This is because of PHP like mechanism. All tasks are rendered everytime Zrb is called)
   - Verbose (i.e., `zrb todo add` instead of `ztadd`)
   - Use can't add argument right away (i.e, `zrb todo add -t "message"`, rather than `zrb todo add "message"`)
```

## Who is the Founder of Bank Sinarmas?

Finally, the AI also capable to use a search engine.

```
Human: Who is the founder of Bank Sinarmas?
Assistant: Eka Tjipta Widjaja is the founder of Bank Sinarmas.
```


# Getting Creative

The Zrb Ollama CLI program is helpful on its own. You can, for example, ask the LLM model to explain a code for you and refactor it.

```bash
zrb-ollama "What this code do? $(cat fibo.py)"
zrb-ollama "Can you make it better?"
```

There are a lot of things you can do with Zrb Ollama.

# Creating Custom PromptTasks

Finally, you can incorporate Zrb Ollama into your [Zrb](https://pypi.org/project/zrb) project workflow. Zrb Ollama introduces a `PromptTask` class that you can use to create more customized LLM tasks.

Let's see an example:

```python
from zrb import runner

from zrb_ollama import PromptTask

chat = PromptTask(
    name="chat",
    input_prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
)
runner.register(chat)
```

## PromptTask Properties

Each PrompTask has the following properties:

- `name (str)`: The name of the task.
- `history_file (str | None)`: Optional file path for storing conversation history.
- `callback_handler_factories (Iterable[CallbackHandlerFactory])`: Factory for creating CallbackHandler.
- `tool_factories (Iterable[ToolFactory])`: Factory for creating tools.
- `llm_factory (LLMFactory | None)`: Factory for creating LLM.
- `prompt_factory (PromptFactory | None)`: Factory for creating prompt.
- `group (Group | None)`: The group to which this task belongs.
- `description (str)`: Description of the task.
- `inputs (List[AnyInput])`: List of inputs for the task.
- `envs (Iterable[Env])`: Iterable of environment variables for the task.
- `env_files (Iterable[EnvFile])`: Iterable of environment files for the task.
- `icon (str | None)`: Icon for the task.
- `color (str | None)`: Color associated with the task.
- `retry (int)`: Number of retries for the task.
- `retry_interval (float | int)`: Interval between retries.
- `upstreams (Iterable[AnyTask])`: Iterable of upstream tasks.
- `checkers (Iterable[AnyTask])`: Iterable of checker tasks.
- `checking_interval (float | int)`: Interval for checking task status.
- `on_triggered (OnTriggered | None)`: Callback for when the task is triggered.
- `on_waiting (OnWaiting | None)`: Callback for when the task is waiting.
- `on_skipped (OnSkipped | None)`: Callback for when the task is skipped.
- `on_started (OnStarted | None)`: Callback for when the task starts.
- `on_ready (OnReady | None)`: Callback for when the task is ready.
- `on_retry (OnRetry | None)`: Callback for when the task retries.
- `on_failed (OnFailed | None)`: Callback for when the task fails.
- `should_execute (bool | str | Callable[..., bool])`: Condition for executing the task.
- `return_upstream_result (bool)`: Flag to return the result of upstream tasks.

## Factories

To understand what factories are for, first, we need to see what a LangChain program looks like:

```python
import os
import sys
from typing import Any

from langchain import hub
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain.prompts import PromptTemplate


tools = [
    Tool(
        name="Search",
        func=DuckDuckGoSearchAPIWrapper().run,
        description="Search engine to answer questions about current events",
    )
]

prompt = hub.pull("hwchase17/react-chat")

llm = ChatOllama(
    model="mistral",
    temperature=0.9,
)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
)

result = agent_executor.invoke(
    {
        # "input": "Who am I?",
        "input": "How many people live in Canada right now?",
        "chat_history": "Human: Hi! My name is Bob\nAI: Hello Bob! Nice to meet you",
    }
)
```

You can see a lot of things going on. But let's focus on the `agent`. You can see that you need a few other components to create an `agent`:

- `llm`
- `tools`
- `prompt`

LangChain allows you to swap the component with anything if the interface matches. For example, you can use bot `OpenAIChat` and `OllamaChat` as `llm`.

PromptTask handles this by allowing you to define how to create elements based on other existing components. Let's see the following pseudo-code:

```python
class PromptTask(AnyPromptTask, BaseTask):
    def __init__(
        self, user_prompt, llm_factory, prompt_factory, tool_factories
    ):
        self.user_prompt = user_prompt
        self.llm_factory = llm_factory
        self.prompt_factory = prompt_factory
        self.tool_factories = tool_factories
    
    def run():
        agent = self.get_agent()
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.get_tools(),
            handle_parsing_errors=True,
        )
        result = agent_executor.invoke(
            {
                # "input": "Who am I?",
                "input": "How many people live in Canada right now?",
                "chat_history": "Human: Hi! My name is Bob\nAI: Hello Bob! Nice to meet you",
            }
        )
        return result["output"]
    
    def get_agent(self):
        return Agent(
            llm=self.get_llm(),
            prompt=self.get_prompt(),
            tools=self.get_tools(),
        )

    @lru_cache(maxsize=1)
    def get_llm(self):
        return self.llm_factory(self) 

    @lru_cache(maxsize=1)
    def get_prompt(self):
        return self.prompt_factory(self)

    @lru_cache(maxsize=1)
    def get_tools(self):
        return [
            tool_factory(self)
            for tool_factory in self.llm_chain_factories
        ]
```

Now, you can control how `get_llm`, `get_prompt`, and `get_tools` behave by setting up the factory properties.

The `lru_cache` also ensures that the getter method will only be called once or less, so you won't lose reference to the components (i.e., when you call `get_llm` twice, the result will refer to the same object).

### How Factories Work

Let's continue with factories:

```python
def ollama_llm_factory(model, temperature):
    def create_ollama_llm(task)
        return ChatOllama(
            model=model,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=temperature,
        ) 
    return create_ollama_llm

def openai_llm_factory(api_key, temperature):
    def create_openai_llm(task)
        return ChatOpenAI(
            api_key,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            streaming=True
            temperature=temperature,
        ) 
    return create_openai_llm


prompt_task = PromptTask(
    user_prompt='Why is the sky blue?',
    llm_factory=ollama_llm_factory(),
    # ...
)
```

We will see how things work in detail by focusing on `PromptTask`'s `run`, `get_agent`, and `get_llm` methods.

```python
class PromptTask(AnyPromptTask, BaseTask):
    # ...
 
    def run(self):
        agent = self.get_agent()
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.get_tools(),
            handle_parsing_errors=True,
        )
        result = agent_executor.invoke(
            {
                # "input": "Who am I?",
                "input": "How many people live in Canada right now?",
                "chat_history": "Human: Hi! My name is Bob\nAI: Hello Bob! Nice to meet you",
            }
        )
        return result["output"]

    def get_agent(self):
        return Agent(
            llm=self.get_llm(),
            prompt=self.get_prompt(),
            tools=self.get_tools(),
        )

    @lru_cache(maxsize=1)
    def get_llm(self):
        return self.llm_factory(self) 

    # ...
```

When Zrb calls `prompt_task.run()`, PromptTask will invoke `get_llm_chain` to get the `llm_chain`.

### The Advantage

By using factories, we create a dependency inversion mechanism. The mechanism allows you to:

- Only create components whenever necessary
- Swap components painlessly
- Implement your custom factory without affecting the other components


# For maintainers

## Publish to pypi

To publish zrb-ollama, you need to have a `Pypi` account:

- Log in or register to [https://pypi.org/](https://pypi.org/)
- Create an API token

You can also create a `TestPypi` account:

- Log in or register to [https://test.pypi.org/](https://test.pypi.org/)
- Create an API token

Once you have your API token, you need to create a `~/.pypirc` file:

```
[distutils]
index-servers =
   pypi
   testpypi

[pypi]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
[testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-xxx-xxx
```

To publish zrb-ollama, you can do the following command:

```bash
zrb plugin publish
```

## Updating version

You can update zrb-ollama version by modifying the following section in `pyproject.toml`:

```toml
[project]
version = "0.0.2"
```

## Adding dependencies

To add zrb-ollama dependencies, you can edit the following section in `pyproject.toml`:

```toml
[project]
dependencies = [
    "Jinja2==3.1.2",
    "jsons==1.6.3"
]
```

## Adding script

To make zrb-package-name executable, you can edit the following section in `pyproject.toml`:

```toml
[project-scripts]
zrb-ollama = "zrb-ollama.__main__:hello"
```

This will look for `hello` callable inside of your `__main__.py` file
