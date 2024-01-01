from zrb import runner
from zrb_ollama import (
    PromptTask, ollama_chat_model_factory, openai_chat_model_factory
)
import os


def choose_chat_model_factory():
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    if openai_api_key != '':
        return openai_chat_model_factory(
            api_key=openai_api_key
        )
    return ollama_chat_model_factory(
        model='mistral',
        temperature=0.8,
        num_gpu=0,
    )


chat = PromptTask(
    name='chat',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    chat_model_factory=choose_chat_model_factory(),
    history_file='.chat-context.json'
)
runner.register(chat)


agent = PromptTask(
    name='agent',
    prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
    system_prompt='You are a code tutor. You eager to explain code in a very detail manner',  # noqa
    chat_model_factory=choose_chat_model_factory(),
    is_agent=True,
    history_file='.agent-context.json'
)
runner.register(agent)
