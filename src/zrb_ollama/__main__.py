from .builtin.install import install
from .task.prompt_task import PromptTask
from .config import DEFAULT_OLLAMA_BASE_URL, OPENAI_API_KEY
from .factory.chat_model import (
    ollama_chat_model_factory, openai_chat_model_factory
)
from .factory.chat_memory import chat_conversation_buffer_window_memory_factory
from .factory.agent_tool import (
    duckduckgo_search_agent_tool_factory, python_repl_agent_tool_factory
)

import os
import sys

_LOCAL_OLLAMA_BASE_URLS = (
    'http://localhost:11434', 'http://0.0.0.0:11434', 'http://127.0.0.1:11434'
)
_HOME_DIR = os.path.expanduser('~')
_AGENT_PROMPT = '''
You are a Python problem solver known for clear and precise solutions.
For each problem, follow these steps:
1. Analyze the problem and devise a Python-based solution.
2. Conduct brief research if necessary to refine your strategy.
3. Develop the solution in Python, focusing on functionality and efficiency.
4. Present your final answer in two distinct parts:
   a. Solution: A succinct, direct response to the problem.
   b. Code: The Python code for the solution, with comments for clarity
   and a print statement to explicitly display the solution.

Example:
Question: Determine the perimeter of a square with each side measuring 2 cm.
Final Answer:
- Solution: The perimeter is 8 cm.
- Code:
  ```python
  # Calculating the perimeter of a square
  side_length = 2
  perimeter = side_length * 4
  # Displaying the solution
  print(perimeter)
  ```
'''


def vanilla_prompt():
    user_prompt = _get_user_prompt()
    prompt_task = PromptTask(
        name='prompt',
        icon='🦙',
        color='light_green',
        prompt=user_prompt,
        system_prompt='',
        chat_model_factory=_chat_model_factory(),
        chat_memory_factory=chat_conversation_buffer_window_memory_factory(
            k=3
        ),
        history_file=os.path.join(_HOME_DIR, '.zrb-ollama-context.json')
    )
    if OPENAI_API_KEY == '' and DEFAULT_OLLAMA_BASE_URL.rstrip('/') in _LOCAL_OLLAMA_BASE_URLS:  # noqa
        prompt_task.add_upstream(install)
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def agent_prompt():
    user_prompt = _get_user_prompt()
    prompt_task = PromptTask(
        name='prompt',
        icon='🦙',
        color='light_green',
        prompt=user_prompt,
        is_agent=True,
        system_prompt=_AGENT_PROMPT,
        chat_model_factory=_chat_model_factory(),
        chat_memory_factory=chat_conversation_buffer_window_memory_factory(
            k=3
        ),
        agent_tool_factories=[
            duckduckgo_search_agent_tool_factory(),
            python_repl_agent_tool_factory()
        ],
        history_file=os.path.join(_HOME_DIR, '.zrb-ollama-context.json')
    )
    if OPENAI_API_KEY == '' and DEFAULT_OLLAMA_BASE_URL.rstrip('/') in _LOCAL_OLLAMA_BASE_URLS:  # noqa
        prompt_task.add_upstream(install)
    prompt_fn = prompt_task.to_function()
    prompt_fn()


def _get_user_prompt():
    if len(sys.argv) > 1:
        return ' '.join(sys.argv[1:])
    return 'Tell me some random fun facts'


def _chat_model_factory():
    if OPENAI_API_KEY != '':
        return openai_chat_model_factory()
    return ollama_chat_model_factory()
