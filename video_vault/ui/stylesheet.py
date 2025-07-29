"""Contains the stylesheet for the application."""

# Color constants
BACKGROUND_DARK = "#221F1F"
TEXT_PRIMARY = "#FFFFFF"
ACCENT_PRIMARY = "#E50914"
ACCENT_HOVER = "#B20710"
ACCENT_PRESSED = "#830F10"
BORDER_SUBTLE = "#555555"

# Font constants
FONT_FAMILY = "'Segoe UI', sans-serif"
FONT_SIZE_BASE = "14px"

# Spacing constants
RADIUS_SMALL = "6px"
PADDING_BUTTON = "10px 20px"
PADDING_MENU = "5px 10px"
SPACING_SEPARATOR = "1px"
MARGIN_SEPARATOR = "10px"

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BACKGROUND_DARK};
    color: {TEXT_PRIMARY};
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE_BASE};
}}

QPushButton {{
    background-color: {ACCENT_PRIMARY};
    color: {TEXT_PRIMARY};
    border: none;
    border-radius: {RADIUS_SMALL};
    padding: {PADDING_BUTTON};
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton:pressed {{
    background-color: {ACCENT_PRESSED};
}}

QMenu {{
    background-color: {ACCENT_PRIMARY};
    color: {TEXT_PRIMARY};
    border: none;
    border-radius: {RADIUS_SMALL};
    padding: {PADDING_MENU};
    font-weight: bold;
}}

QMenu::item {{
    padding: {PADDING_MENU};
}}

QMenu::item:selected {{
    background-color: {ACCENT_HOVER};
}}

QMenu::item:hover {{
    background-color: {ACCENT_HOVER};
}}

QMenu::separator {{
    height: {SPACING_SEPARATOR};
    background: {BORDER_SUBTLE};
    margin-left: {MARGIN_SEPARATOR};
    margin-right: {MARGIN_SEPARATOR};
}}
"""
