"""module."""

from winipedia_utils.dev.projects.poetry.poetry import get_poetry_run_cli_cmd_args
from winipedia_utils.utils.os.os import run_subprocess
from winipedia_utils.utils.testing.assertions import assert_with_msg


def test_run() -> None:
    """Test func for run."""
    # call --help and verify it doesn't error
    completed_process = run_subprocess([*get_poetry_run_cli_cmd_args(), "--help"])
    assert_with_msg(completed_process.returncode == 0, "Should not error")
    stdout = completed_process.stdout.decode("utf-8")
    assert_with_msg("Run the app" in stdout, "Should show run command")
