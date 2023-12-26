# Zrb ollama

zrb-ollama is a [pypi](https://pypi.org) package.

You can install zrb-ollama by invoking the following command:

```bash
# From pypi
pip install zrb-ollama
# From github
pip install git+https://github.com/goFrendiAsgard/zrb-ollama.git@main
# From directory
pip install path/to/this/directory
```

Once zrb-ollama is installed, you can then run it by invoking the following command:

```bash
zrb-ollama "Why is the sky blue?"
```

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
zrb project publish-zrb-ollama
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
