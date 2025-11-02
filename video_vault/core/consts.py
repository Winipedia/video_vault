"""This module contains constants for the application."""

from winipedia_utils.projects.poetry.config import PyprojectConfigFile
from winipedia_utils.text.string import make_name_from_obj

import video_vault

APP_NAME = make_name_from_obj(video_vault, split_on="_", join_on="", capitalize=True)

AUTHOR = PyprojectConfigFile.get_main_author_name()
