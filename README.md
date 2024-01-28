![](https://raw.githubusercontent.com/goFrendiAsgard/zrb-ollama/main/_images/android-chrome-192x192.png)

# Zrb Ollama

Zrb Ollama is a [pypi](https://pypi.org) package that acts as Ollama and LangChain wrapper, allowing you to incorporate LLM into your workflow.

# Installation

You can install Zrb Ollama by invoking any of the following commands:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/goFrendiAsgard/zrb-ollama.git@main
# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

By default, Zrb Ollama uses Ollama-based LLM. You can install Ollama by visiting the official website: [`https://ollama.ai/`](https://ollama.ai/).

You can, however, change this behavior by setting `OPENAI_API_KEY`. When `OPENAI_API_KEY` is present, Zrb Ollama will use the Open AI API instead.

# Configuration

You can configure Zrb Ollama using a few environment variables:

- `ZRB_DEFAULT_LLM_PROVIDER`: LLM Provider (i.e., `ollama`, `openai`, `bedrock`). If not specified, Zrb Ollama will use `ollama`
- `ZRB_OLLAMA_BASE_URL`: Default Ollama base URL. If not specified, Zrb Ollama will use `http://localhost:11434`.
- `ZRB_OLLAMA_DEFAULT_MODEL`: Default Ollama model. If not specified, Zrb Ollama will use `mistral`.
- `OPENAI_API_KEY`
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`

# Talk to Zrb Ollama

Zrb Ollama provides a simple CLI command to interact with the LLM. This CLI command also manages your chat history and saves everything under `~/.zrb-ollama-context.json`.

Let's see the following example:

```bash
zrb-ollama "Why is the sky blue?"
```

<details>
<summary>👇See the output</summary>

```
The sky appears blue due to a phenomenon called Rayleigh scattering. When sunlight enters Earth's atmosphere, it encounters molecules and tiny particles in the air. The shorter wavelengths of light, such as blue and violet, are scattered more strongly by these particles compared to the longer wavelengths of light, like red and orange. As a result, the blue light gets scattered in all directions, creating the blue appearance of the sky.
```

</details>

Zrb Ollama will explain why the sky is blue.

Next, you can ask it to give a more detailed explanation:

```bash
zrb-ollama "Explain in more detailed"
```

<details>
<summary>👇See the output</summary>

```
Sure! When sunlight reaches Earth's atmosphere, it is composed of different colors of light, each with a different wavelength. The shorter wavelengths, such as blue and violet, have higher energy, while the longer wavelengths, such as red and orange, have lower energy.

As sunlight enters the atmosphere, it interacts with the molecules and tiny particles present in the air. These particles include nitrogen and oxygen molecules, as well as dust, water droplets, and other small particles.

The interaction between the sunlight and these particles causes a scattering of light. This scattering process is known as Rayleigh scattering. It is named after the British physicist Lord Rayleigh, who first explained it in the 19th century.

Rayleigh scattering occurs when the size of the particles in the atmosphere is much smaller than the wavelength of light. In this case, the scattering is inversely proportional to the fourth power of the wavelength. This means that shorter wavelengths, such as blue and violet light, are scattered much more strongly than longer wavelengths, such as red and orange light.

As a result, when sunlight enters the atmosphere, the blue and violet light is scattered in all directions by the particles in the air. This scattered blue light then reaches our eyes from all parts of the sky, making it appear blue to us.

It's important to note that the scattering of light is not limited to just the blue color. However, since our eyes are more sensitive to blue light, we perceive the scattered blue light more prominently, hence the blue appearance of the sky.

At sunrise or sunset, when the sun is lower in the sky, the sunlight has to pass through a larger portion of the atmosphere before reaching us. This longer path causes more scattering and absorption of shorter wavelengths, like blue and violet light, resulting in the red, orange, and pink hues commonly seen during these times.

In summary, the sky appears blue due to Rayleigh scattering, where the shorter wavelengths of sunlight, particularly blue and violet light, are scattered more strongly by the particles in the atmosphere, making the scattered blue light dominant in our perception.
```

</details>

It will understand that you asked for a more detailed explanation of why the sky is blue.

# Talk is Cheap, Show Me The Code

Furthermore, Zrb Ollama also allows you to use an AI Agent. This AI Agent can access the internet and interact with the Python interpreter.

Zrb Ollama Agent will show you the reasoning process, the solution, and the respecting Python code.

Note that for this to work, you need better LLM models like `Mistral` or Open AI.

Let's see the following example:

```bash
# You can use Ollama's mistral model:
# export ZRB_OLLAMA_DEFAULT_MODEL=mistral

# or you can use Open AI:
export OPENAI_API_KEY=your-api-key
export DEFAULT_LLM_PROVIDER=openai

zrb-ollama-agent "What is the area of a square with 20 cm perimeter?"
```

<details>
<summary>👇See the output</summary>

```
Thought: To find the area of a square, we need to know the side length. We can calculate the side length by dividing the perimeter by 4. Once we have the side length, we can use the formula for the area of a square, which is side length squared.

    Action: Python code

    ```python
    # Calculating the area of a square
    perimeter = 20
    side_length = perimeter / 4
    area = side_length ** 2
    # Displaying the solution
    print(area)
    ```
    I need to provide the input for the action, which is the value of the perimeter.

    Action: python_repl
    Action Input: 20
    The code executed successfully and provided the expected output.

    Final Answer:
    - Solution: The area of a square with a perimeter of 20 cm is 25 square centimeters.
    - Code:
      ```python
      # Calculating the area of a square
      perimeter = 20
      side_length = perimeter / 4
      area = side_length ** 2
      # Displaying the solution
      print(area)
      ```
```

</details>

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
