from zrb import runner
from zrb_ollama import PromptTask, ollama_chat_model_factory

chat = PromptTask(
    name='chat',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    chat_model_factory=ollama_chat_model_factory(
        model='mistral',
        temperature=0.8,
        num_gpu=0,
    ),
    history_file='.ctx.json'
)
runner.register(chat)
