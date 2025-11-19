"""This module contains constants for the application."""

from pyrig.src.string import make_name_from_obj

import video_vault

APP_NAME = make_name_from_obj(video_vault, split_on="_", join_on="", capitalize=True)

AUTHOR = "Winipedia"
