# Zrb Ollama

zrb-ollama is a [pypi](https://pypi.org) package that acts as Ollama's wrapper, allowing you to incorporate LLM into your workflow.

## Installation

You can install zrb-ollama by invoking the following command:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/goFrendiAsgard/zrb-ollama.git@main
# From directory
pip install --use-feature=in-tree-build path/to/this/directory
```

## Run Zrb Ollama

Once you install zrb-ollama, you can then run it by invoking the following command:

```bash
zrb-ollama "Why is the sky blue?"
```

When you talk to zrb-ollama, it will save your context history in `~/.zrb-ollama-context.json`. Thus, you can continue the conversation and retain the context. For example, you can ask `zrb-ollama "Explain in more detail"`.

## Creating a PromptTask

You can also import `zrb-ollama` into your Zrb project and perform some fun things:

```python
from zrb import runner
from zrb_ollama import PromptTask

chat = PromptTask(
    name='chat',
    model='mistral',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    options={
        'temperature': 0.8,
        'num_gpu': 0
    },
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    context_file='.ctx.json'
)
runner.register(chat)
```

```
zrb chat "Please explain the following Python script: $(cat fibo.py)"
zrb chat "Can you make it better?"
```

# Configuration

You can configure Zrb Ollama using a few environment variables:

- `ZRB_OLLAMA_BASE_URL`: Default Ollama base URL. if not specified, Zrb Ollama will use `http://localhost:11434`.
- `ZRB_OLLAMA_DEFAULT_MODEL`: Default Ollama model. If not specified, Zrb Ollama will use `mistral`.


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
