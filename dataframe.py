"""
Creates a pandas dataframe containing all the information we will possibly need.
"""
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import json
import os


def create_megaframe():    
    megaframe = pd.DataFrame()
    files = os.listdir('./inbox/valerie_0p9yu22iaq')

    for file in files:
        if file.endswith(".json"):
            with open(f'./inbox/valerie_0p9yu22iaq/{file}') as json_file:
                json_data = json.load(json_file)
                df = pd.DataFrame(json_data['messages'])
                megaframe = pd.concat([megaframe, df])
    
    # converting unix datetime into datetime objects
    megaframe['timestamp_ms'] = pd.to_datetime(megaframe['timestamp_ms'], unit='ms')
    
    # dropping unnecessary data
    megaframe.drop(['share', 'photos', 'reactions', 'videos', 'audio_files'], axis=1, inplace=True)
    
    return megaframe