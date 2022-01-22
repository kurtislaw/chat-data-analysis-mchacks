"""
Individuals
"""
import os
from typing import Tuple


# 1. Selector
# 2. Analysis

# def lists_all_friends() -> tuple:
#     """Returns a tuple containing all friends in the messages folder."""
#     rootdir = '/messages/'


def list_all_directories() -> Tuple[str]:
    """Returns all the directories as tuples containing strings"""
    root_dir = "./messages/"
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            print(os.path.join(subdir, file))