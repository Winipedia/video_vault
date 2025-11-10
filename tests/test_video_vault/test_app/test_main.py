"""module."""

from pytest_mock import MockerFixture
from winipedia_utils.utils.modules.module import make_obj_importpath
from winipedia_utils.utils.testing.assertions import assert_with_msg

from video_vault.app import main as main_module
from video_vault.app.main import main


def test_main(mocker: MockerFixture) -> None:
    """Test func for main."""
    # Mock QApplication and its methods
    mock_app = mocker.Mock()
    mock_qapplication = mocker.patch(make_obj_importpath(main_module) + ".QApplication")
    mock_qapplication.return_value = mock_app

    # Mock sys.argv
    mock_sys = mocker.patch(make_obj_importpath(main_module) + ".sys")
    mock_sys.argv = ["video_vault"]

    # Mock the stylesheet
    mock_stylesheet = "fake stylesheet content"
    mocker.patch(make_obj_importpath(main_module) + ".STYLESHEET", mock_stylesheet)

    # Mock the VideoVault window
    mock_window = mocker.Mock()
    mock_videovault_window = mocker.patch(
        make_obj_importpath(main_module) + ".VideoVaultWindow"
    )
    mock_videovault_window.return_value = mock_window

    # Call the main function
    main()

    # Verify QApplication was created with sys.argv
    mock_qapplication.assert_called_once_with(["video_vault"])

    # Verify stylesheet was set
    mock_app.setStyleSheet.assert_called_once_with(mock_stylesheet)

    # Verify VideoVault window was created
    mock_videovault_window.assert_called_once()

    # Verify window was shown maximized
    mock_window.showMaximized.assert_called_once()

    # Verify app.exec() was called to start the event loop
    mock_app.exec.assert_called_once()


def test_main_integration(mocker: MockerFixture) -> None:
    """Test func for main with integration testing approach."""
    # Mock the VideoVault window to avoid actual window creation
    mock_window = mocker.Mock()
    mock_videovault_window = mocker.patch(
        make_obj_importpath(main_module) + ".VideoVaultWindow"
    )
    mock_videovault_window.return_value = mock_window

    # Mock app.exec() to prevent blocking
    mock_app_exec = mocker.patch(
        make_obj_importpath(main_module) + ".QApplication.exec"
    )

    # Mock the stylesheet
    mock_stylesheet = "test stylesheet"
    mocker.patch(make_obj_importpath(main_module) + ".STYLESHEET", mock_stylesheet)

    # Call the main function
    main()

    # Verify the window was created and configured
    mock_videovault_window.assert_called_once()
    mock_window.showMaximized.assert_called_once()
    mock_app_exec.assert_called_once()


def test_main_stylesheet_integration(mocker: MockerFixture) -> None:
    """Test that main function properly integrates with the stylesheet."""
    # Mock QApplication and its methods
    mock_app = mocker.Mock()
    mock_qapplication = mocker.patch(make_obj_importpath(main_module) + ".QApplication")
    mock_qapplication.return_value = mock_app

    # Mock the VideoVault window
    mock_window = mocker.Mock()
    mock_videovault_window = mocker.patch(
        make_obj_importpath(main_module) + ".VideoVaultWindow"
    )
    mock_videovault_window.return_value = mock_window

    # Use the actual STYLESHEET import to test integration
    # (Don't mock it to test the real import)

    # Call the main function
    main()

    # Verify setStyleSheet was called (with whatever the actual stylesheet is)
    mock_app.setStyleSheet.assert_called_once()

    # Verify the stylesheet argument is a string
    call_args = mock_app.setStyleSheet.call_args[0]
    assert_with_msg(isinstance(call_args[0], str), "Stylesheet should be a string")
