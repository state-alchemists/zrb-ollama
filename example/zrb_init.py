from zrb import runner, CmdTask, StrInput
from zrb_ollama import LLMTask
from zrb_ollama.tools import query_internet, create_rag, get_git_diff

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
        create_rag(
            documents=[get_article],
            # model="text-embedding-ada-002",
            model=_EMBEDDING_MODEL,
            rag_description="Look for anything related to John Titor",
            vector_db_path=os.path.join(_CURRENT_DIR, "john-titor-vector"),
        ),
        query_internet,
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
        StrInput(
            name="user-prompt",
            default="In ./sample-repo, code review the changes on feat/iterative branch relative to main branch. Make suggestions if necessary."  # noqa
        ),
    ],
    # model="gpt-4o",
    model=_MODEL,
    user_message="{{input.user_prompt}}",
    tools=[
        get_git_diff,
        query_internet,
    ],
)
prepare_repo >> code_review
runner.register(code_review)
