from .calculate import calculate
from .get_current_location import get_current_location
from .get_current_weather import get_current_weather
from .git import get_git_diff
from .query_internet import query_internet
from .run_shell_command import run_shell_command
from .rag import create_rag

assert create_rag
assert calculate
assert get_current_location
assert get_current_weather
assert get_git_diff
assert query_internet
assert run_shell_command
