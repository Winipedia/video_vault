"""This module contains constants for the application."""

from winipedia_utils.modules.package import make_name_from_package
from winipedia_utils.projects.poetry.config import PyprojectConfigFile

import video_vault

APP_NAME = make_name_from_package(
    video_vault, split_on="_", join_on="", capitalize=True
)

AUTHOR = PyprojectConfigFile.get_main_author_name()
