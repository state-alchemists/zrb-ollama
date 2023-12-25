from zrb import runner
from zrb_ollama import PromptTask

fun_fact = PromptTask(
    name='fun-fact',
    model='mistral:cpu',
    prompt='Tell some fun-fact',
)
runner.register(fun_fact)
