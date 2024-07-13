from zrb import runner, CmdTask, StrInput
from zrb_ollama import LLMTask, ToolFactory
from zrb_ollama.tools import query_internet, create_rag, create_get_changes

import os

_CURRENT_DIR = os.path.dirname(__file__)
_MODEL = os.getenv("EXAMPLE_MODEL", "ollama/mistral:7b-instruct")
_EMBEDDING_MODEL = os.getenv("EXAMPLE_EMBEDDING_MODEL", "ollama/nomic-embed-text")


##################################################################################
# RAG Demo
##################################################################################

def get_article():
    with open(os.path.join(_CURRENT_DIR, "john-titor.md")) as f:
        return f.read()


rag = LLMTask(
    name="rag",
    inputs=[
        StrInput(name="user-prompt", default="How John Titor introduce himself?"),
    ],
    # model="gpt-4o",
    model=_MODEL,
    user_message="{{input.user_prompt}}",
    tools=[
        query_internet
    ],
    tool_factories=[
        ToolFactory(
            create_rag,
            tool_name="retrieve_john_titor_info",
            tool_description="Look for anything related to John Titor",
            documents=[get_article],
            # model="text-embedding-ada-002",
            model=_EMBEDDING_MODEL,
            vector_db_path=os.path.join(_CURRENT_DIR, "john-titor-vector"),
        )
    ]
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
            default="In .sample-repo, code review the changes and make suggestions if necessary."  # noqa
        ),
    ],
    # model="gpt-4o",
    model=_MODEL,
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
    ]
)
prepare_repo >> code_review
runner.register(code_review)
