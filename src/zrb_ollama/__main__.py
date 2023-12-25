WELCOME_STR = '''

This is a zrb ollama plugin.
You can use zrb_ollama by importing it to your zrb_init.py

```python
from zrb import runner
from zrb_ollama import OllamaTask

task = OllamaTask(
    name='eval',
    model='mistral',
    inputs=[
        StrInput(name='prompt')
    ],
    prompt='{{input.prompt}}'
)
```
'''


def hello():
    print(WELCOME_STR)
