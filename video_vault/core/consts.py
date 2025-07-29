"""This module contains constants for the application."""

from winipedia_utils.projects.project import make_name_from_package

import video_vault

APP_NAME = make_name_from_package(
    video_vault, split_on="_", join_on="", capitalize=True
)

AUTHOR = "Winipedia"
