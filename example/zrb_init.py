import os

from zrb import CmdTask, StrInput, runner
from zrb_ollama import LLMTask, ToolFactory
from zrb_ollama.tools import (
    create_get_changes, create_rag, documents_from_directory, query_internet
)

_CURRENT_DIR = os.path.dirname(__file__)
_RAG_DIR = os.path.join(_CURRENT_DIR, "rag")


##################################################################################
# RAG Demo
##################################################################################

rag = LLMTask(
    name="rag",
    inputs=[
        StrInput(name="user-prompt", default="How John Titor introduce himself?"),
    ],
    # model="gpt-4o",
    user_message="{{input.user_prompt}}",
    tools=[query_internet],
    tool_factories=[
        ToolFactory(
            create_rag,
            tool_name="retrieve_john_titor_info",
            tool_description="Look for anything related to John Titor",
            documents=documents_from_directory(os.path.join(_RAG_DIR, "document")),
            # model="text-embedding-ada-002",
            vector_db_path=os.path.join(_RAG_DIR, "vector"),
            # reset_db=True,
        )
    ],
)
runner.register(rag)


##################################################################################
# Code Review Demo
##################################################################################

prepare_repo = CmdTask(
    name="prepare-repo",
    cwd=_CURRENT_DIR,
    cmd=[
        "rm -Rf sample-repo",
        "mkdir sample-repo",
        "cd sample-repo",
        "git init",
        "git branch -M main",
        "cp ../sample-template/recursive-fibo.js ./fibonacci.js",
        "git add . -A",
        "git commit -m 'First commit'",
        "git checkout -b 'feat/iterative'",
        "cp ../sample-template/iterative-fibo.js ./fibonacci.js",
        "git add . -A",
        "git commit -m 'Make it into iterative'",
    ],
)

code_review = LLMTask(
    name="code-review",
    inputs=[
        StrInput(name="directory", default="./sample-repo"),
        StrInput(name="initial-branch", default="main"),
        StrInput(name="new-branch", default="feat/iterative"),
        StrInput(
            name="user-prompt",
            default="In .sample-repo, code review the changes and make suggestions if necessary.",  # noqa
        ),
    ],
    # model="gpt-4o",
    user_message="{{input.user_prompt}}",
    tools=[
        query_internet,
    ],
    tool_factories=[
        ToolFactory(
            create_get_changes,
            tool_name="get_sample_repo_changes",
            tool_description="Get git diff of sample repo",
            directory="{{input.directory}}",
            initial_branch="{{input.initial_branch}}",
            new_branch="{{input.new_branch}}",
        )
    ],
)
prepare_repo >> code_review
runner.register(code_review)
