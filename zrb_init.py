import os

from zrb import CmdTask, StrInput, runner
from zrb.builtin.group import plugin_group

PROJECT_DIR = os.path.dirname(__file__)

###############################################################################
# ⚙️ prepare-plugin
###############################################################################

prepare = CmdTask(
    name="prepare",
    group=plugin_group,
    description="Prepare venv for plugin",
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, "_cmd", "activate-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "prepare-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "format.sh"),
    ],
)
runner.register(prepare)

###############################################################################
# ⚙️ build-plugin
###############################################################################

build = CmdTask(
    name="build",
    group=plugin_group,
    description="Build plugin",
    upstreams=[prepare],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, "_cmd", "activate-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "build.sh"),
    ],
)
runner.register(build)

###############################################################################
# ⚙️ publish-plugin
###############################################################################

publish = CmdTask(
    name="publish",
    group=plugin_group,
    description="Publish plugin",
    inputs=[
        StrInput(
            name="plugin-repo",
            prompt="Pypi repository for plugin",
            description="Pypi repository for human readalbe zrb package name",
            default="pypi",
        )
    ],
    upstreams=[build],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, "_cmd", "activate-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "publish.sh"),
    ],
)
runner.register(publish)

###############################################################################
# ⚙️ install-symlink
###############################################################################

install_symlink = CmdTask(
    name="install-symlink",
    group=plugin_group,
    description="Install plugin as symlink",
    upstreams=[build],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, "_cmd", "activate-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "install-symlink.sh"),
    ],
)
runner.register(install_symlink)

###############################################################################
# ⚙️ prepare-playground
###############################################################################

prepare_playground = CmdTask(
    name="prepare-playground",
    group=plugin_group,
    description="Prepare playground",
    upstreams=[prepare],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, "_cmd", "activate-venv.sh"),
        os.path.join(PROJECT_DIR, "_cmd", "prepare-playground.sh"),
    ],
)
runner.register(prepare_playground)

###############################################################################
# ⚙️ test-playground
###############################################################################

test_playground = CmdTask(
    name="test-playground",
    group=plugin_group,
    description="Test playground",
    upstreams=[prepare_playground],
    cwd=os.path.join(PROJECT_DIR, "playground"),
    cmd_path=os.path.join(PROJECT_DIR, "_cmd", "test-playground.sh"),
)
runner.register(test_playground)
