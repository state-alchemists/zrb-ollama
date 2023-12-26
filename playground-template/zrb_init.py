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
