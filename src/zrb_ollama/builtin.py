from zrb import runner, Group, CmdTask

import os

CURRENT_DIR = os.path.dirname(__file__)
CMD_PATH = os.path.join(CURRENT_DIR, 'cmd')
DEFAULT_MODEL = os.getenv('ZRB_OLLAMA_DEFAULT_MODEL', 'mistral')

ollama_group = Group(name='ollama', description='ollama')

install = CmdTask(
    name='install',
    group=ollama_group,
    cmd_path=os.path.join(CMD_PATH, 'install.sh'),
    preexec_fn=None
)


runner.register(install)
