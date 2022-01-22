"""
Filters the messages.zip file into useful data
"""
from zipfile import ZipFile

def extract_zip(directory: str):
    with ZipFile(directory, 'r') as zip:
        zip.extractall()