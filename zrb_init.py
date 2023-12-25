from zrb import CmdTask, runner, StrInput

import os

PROJECT_DIR = os.path.dirname(__file__)

###############################################################################
# ⚙️ prepare-plugin
###############################################################################

prepare_plugin = CmdTask(
    name='prepare-plugin',
    description='Prepare venv for plugin',
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, '_cmd', 'activate-venv.sh'),
        os.path.join(PROJECT_DIR, '_cmd', 'prepare-venv.sh'),
    ]
)
runner.register(prepare_plugin)

###############################################################################
# ⚙️ build-plugin
###############################################################################

build_plugin = CmdTask(
    name='build-plugin',
    description='Build plugin',
    upstreams=[prepare_plugin],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, '_cmd', 'activate-venv.sh'),
        os.path.join(PROJECT_DIR, '_cmd', 'build.sh'),
    ]
)
runner.register(build_plugin)

###############################################################################
# ⚙️ publish-plugin
###############################################################################

publish_plugin = CmdTask(
    name='publish-plugin',
    description='Publish plugin',
    inputs=[
        StrInput(
            name='plugin-repo',
            prompt='Pypi repository for plugin',
            description='Pypi repository for human readalbe zrb package name',
            default='pypi',
        )
    ],
    upstreams=[build_plugin],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, '_cmd', 'activate-venv.sh'),
        os.path.join(PROJECT_DIR, '_cmd', 'publish.sh'),
    ]
)
runner.register(publish_plugin)

###############################################################################
# ⚙️ install-kebab-zrb-task-name-symlink
###############################################################################

install_plugin_symlink = CmdTask(
    name='install-plugin-symlink',
    description='Install plugin as symlink',
    upstreams=[build_plugin],
    cwd=PROJECT_DIR,
    cmd_path=[
        os.path.join(PROJECT_DIR, '_cmd', 'activate-venv.sh'),
        os.path.join(PROJECT_DIR, '_cmd', 'install-symlink.sh'),
    ]
)
runner.register(install_plugin_symlink)
