"""module."""

from pytest_mock import MockerFixture
from winipedia_utils.utils.modules.module import make_obj_importpath

from video_vault.dev.cli import subcommands
from video_vault.dev.cli.subcommands import run


def test_run(mocker: MockerFixture) -> None:
    """Test func for run."""
    mock_main = mocker.patch(make_obj_importpath(subcommands) + ".main")
    run()
    mock_main.assert_called_once()
