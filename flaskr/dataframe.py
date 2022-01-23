"""
Creates a pandas dataframe containing all the information we will possibly need.
"""
import pandas as pd
import json
import os


#####################################################################################
# A megaframe containing all relevant data for a SINGLE person's conversation JSON
#####################################################################################
def create_participants_dataframe(dir: str):
    """
    Receives a directory str and returns a participants pandas dataframe.
    """
    participants = pd.DataFrame()
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".json"):
            with open(f'{dir}/{file}') as json_file:
                json_data = json.load(json_file)
                pt = pd.DataFrame(json_data['participants'])
                participants = pd.concat([participants, pt]).drop_duplicates().reset_index(drop=True)

    return participants


def create_message_dataframe(dir: str):
    """
    Receives a directory str and returns a messages pandas dataframe.

    Example dir:
        - './inbox/FOLDER/'
    """
    messages = pd.DataFrame()
    files = os.listdir(dir)

    for file in files:
        if file.endswith(".json"):
            with open(f'{dir}/{file}') as json_file:
                json_data = json.load(json_file)
                ms = pd.DataFrame(json_data['messages'])
                messages = pd.concat([messages, ms])

    # converting unix datetime into datetime objects
    messages['timestamp_ms'] = pd.to_datetime(
        messages['timestamp_ms'], unit='ms')

    # dropping unnecessary data
    useless_columns = ['share', 'photos', 'reactions', 'videos', 'audio_files']
    for column in useless_columns:
        if column in messages.columns:
            messages.drop(column, axis=1, inplace=True)

    return messages
