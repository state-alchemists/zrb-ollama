import json
import subprocess


def create_get_changes(
    tool_name: str,
    tool_description: str,
    initial_branch: str,
    new_branch: str,
    directory: str,
):
    def get_changes() -> str:
        # Fetch the latest changes in the specified directory
        subprocess.run(["git", "fetch"], cwd=directory, check=True)
        # Get the diff between the two branches in the specified directory
        result = subprocess.run(
            ["git", "diff", f"{initial_branch}..{new_branch}"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
        )
        diff_output = result.stdout
        # Initialize an empty list to store the dictionaries
        diff_list = []
        # Split the diff output by file
        file_diffs = diff_output.split("diff --git")
        for file_diff in file_diffs:
            if file_diff.strip() == "":
                continue
            # Extract the file path
            lines = file_diff.split("\n")
            file_path = lines[0].split(" ")[-1][2:]  # Extract the path after "b/"
            # Join the lines to get the full diff for the file
            changes = "\n".join(lines[1:])
            # Get the current content of the file in the new branch
            file_content_result = subprocess.run(
                ["git", "show", f"{new_branch}:{file_path}"],
                cwd=directory,
                capture_output=True,
                text=True,
                check=True,
            )
            current_content = file_content_result.stdout
            # Create a dictionary for the file
            file_dict = {
                "file_path": file_path,
                "changes": changes,
                "current_content": current_content,
            }
            # Add the dictionary to the list
            diff_list.append(file_dict)
        return json.dumps(diff_list)

    get_changes.__name__ = tool_name
    get_changes.__doc__ = tool_description
    return get_changes
