import subprocess

from modules.colors import GREEN, RED, RESET


def update_project():
    from pathlib import Path
    from shutil import which

    if which("git") is None:
        return f"{RED}Git is not installed!{RESET}"

    project_dir = Path(__file__).parent.parent

    try:
        subprocess.run(
            ["git", "-C", str(project_dir), "pull"],
            check=True,
            capture_output=True,
            text=True,
            shell=False,
        )
        return f"{GREEN}Project updated successfully!{RESET}"
    except subprocess.CalledProcessError as e:
        return f"{RED}Update failed: {e.stderr}{RESET}"
