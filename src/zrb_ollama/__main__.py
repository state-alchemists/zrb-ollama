import asyncio
import os
import sys

from zrb.helper.loader.load_module import load_module
from zrb.helper.loader.load_script import load_script

from .config import INIT_MODULES, INIT_SCRIPTS
from .interactive import Conversation, interactive_tools


def prompt():
    for init_module in INIT_MODULES:
        load_module(init_module)
    for init_script in INIT_SCRIPTS:
        load_script(init_script)
    default_init_script = os.path.abspath("./zrb_ollama_init.py")
    if os.path.exists(default_init_script):
        load_script(default_init_script)
    initial_user_input = "" if len(sys.argv) <= 1 else " ".join(sys.argv[1:])
    conversation = Conversation(
        enabled_tool_names=interactive_tools.get_enabled_tool_names(),
        available_tools=interactive_tools.get_available_tools(),
        initial_user_input=initial_user_input,
    )
    asyncio.run(conversation.loop())
