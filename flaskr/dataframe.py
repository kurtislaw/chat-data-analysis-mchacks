"""
Creates a pandas dataframe containing all the information we will possibly need.
"""
import pandas as pd
import json
import os


#####################################################################################
# A megaframe containing all relevant data for a SINGLE person's conversation JSON
#####################################################################################


def create_megaframe(dir: str):
    """
    Receives a directory str and returns a pandas dataframe. 

    Example dir:
        - './inbox/FOLDER/'
    """
    dataframe = pd.DataFrame()
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".json"):
            with open(f'{dir}/{file}') as json_file:
                json_data = json.load(json_file)
                df = pd.DataFrame(json_data['messages'])
                dataframe = pd.concat([dataframe, df])

    # converting unix datetime into datetime objects
    dataframe['timestamp_ms'] = pd.to_datetime(
        dataframe['timestamp_ms'], unit='ms')

    # dropping unnecessary data
    useless_columns = ['share', 'photos', 'reactions', 'videos', 'audio_files']
    for column in useless_columns:
        if column in dataframe.columns:
            dataframe.drop(column, axis=1, inplace=True)

    return dataframe
