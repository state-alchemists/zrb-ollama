import os
import subprocess

from zrb import CmdTask, runner

from zrb_ollama.group import ollama_group

CURRENT_DIR = os.path.dirname(__file__)
CMD_PATH = os.path.join(CURRENT_DIR, "cmd")


def _should_install_ollama() -> bool:
    try:
        subprocess.run(
            ["ollama", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return False
    except subprocess.CalledProcessError:
        return True


install = CmdTask(
    name="install",
    group=ollama_group,
    cmd="curl https://ollama.ai/install.sh | sh",
    preexec_fn=None,
    should_execute=_should_install_ollama(),
)

runner.register(install)
