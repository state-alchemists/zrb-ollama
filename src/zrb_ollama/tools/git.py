import subprocess


def get_git_diff(initial_branch: str, new_branch: str, directory: str) -> str:
    """
    Get git difference between two branches
    """
    # Fetch the latest changes in the specified directory
    subprocess.run(['git', 'fetch'], cwd=directory, check=True)
    # Get the diff between the two branches in the specified directory
    result = subprocess.run(
        ['git', 'diff', f'{initial_branch}..{new_branch}'],
        cwd=directory, capture_output=True, text=True, check=True
    )
    return result.stdout