"""
Path Utilities

Utility functions for path operations.
"""

import os


def get_project_root() -> str:
    """Get the project root directory.
    
    Returns:
        Absolute path to the project root directory
    """
    # Get the directory containing this file (gui_app/utils/)
    # Go up two levels to get project root
    current_file = os.path.abspath(__file__)
    utils_dir = os.path.dirname(current_file)
    gui_app_dir = os.path.dirname(utils_dir)
    project_root = os.path.dirname(gui_app_dir)
    return project_root
