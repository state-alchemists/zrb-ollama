from zrb_ollama.group import ollama_group
from zrb import runner, CmdTask

import os

CURRENT_DIR = os.path.dirname(__file__)
CMD_PATH = os.path.join(CURRENT_DIR, 'cmd')

install = CmdTask(
    name='install',
    group=ollama_group,
    cmd_path=os.path.join(CMD_PATH, 'install.sh'),
    preexec_fn=None
)

runner.register(install)
