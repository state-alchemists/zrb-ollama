import asyncio
import os
import sys

from .interactive import interactive_tools, load_module, Conversation
from .config import INIT_SCRIPTS


def prompt():
    for init_script in INIT_SCRIPTS:
        load_module(init_script)
    default_init_script = os.path.abspath("./zrb_ollama_init.py")
    if os.path.exists(default_init_script):
        load_module(default_init_script)
    initial_user_input = "" if len(sys.argv) <= 1 else " ".join(sys.argv[1:])
    conversation = Conversation(
        enabled_tool_names=interactive_tools.get_enabled_tool_names(),
        available_tools=interactive_tools.get_available_tools(),
        initial_user_input=initial_user_input
    )
    asyncio.run(conversation.loop())
