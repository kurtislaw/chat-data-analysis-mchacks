"""
Creates a pandas dataframe containing all the information we will possibly need.
"""
import pandas as pd
from matplotlib import pyplot as plt, use
from matplotlib.pyplot import figure
import numpy as np
import json
import os

# message_1.json


def create_megaframe(dir: str):
    """
    Set up dataframe from file directory.
    """
    megaframe = pd.DataFrame()
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".json"):
            with open(f'{dir}/{file}') as json_file:
                json_data = json.load(json_file)
                df = pd.DataFrame(json_data['messages'])
                megaframe = pd.concat([megaframe, df])
    
    # converting unix datetime into datetime objects
    megaframe['timestamp_ms'] = pd.to_datetime(megaframe['timestamp_ms'], unit='ms')
    
    # dropping unnecessary data
    useless_columns = ['share', 'photos', 'reactions', 'videos', 'audio_files']
    for column in useless_columns:
        if column in megaframe.columns:
            megaframe.drop(column, axis=1, inplace=True)

    return megaframe
