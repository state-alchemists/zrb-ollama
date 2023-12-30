from zrb import runner
from zrb_ollama import PromptTask

chat = PromptTask(
    name='chat',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    ollama_model='mistral',
    ollama_temperature=0.8,
    ollama_num_gpu=0,
    ollama_system='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    history_file='.ctx.json'
)
runner.register(chat)
