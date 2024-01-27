from zrb import runner

from zrb_ollama import PromptTask

chat = PromptTask(
    name="chat",
    input_prompt='echo {{ " ".join(input._args) if input._args | length > 0 else "tell me some fun fact" }}',  # noqa
)
runner.register(chat)
