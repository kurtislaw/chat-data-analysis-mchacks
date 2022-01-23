"""
Individuals
"""


import pandas as pd
from flaskr import dataframe
from flask import request
import plotly.io as pio
from glob import glob
from collections import Counter
from nltk.corpus import stopwords
import datetime

pio.renderers.default = "browser"
pd.options.plotting.backend = 'plotly'


def find_all_names() -> dict:
    """Parses through inbox directory, returns the names of all people."""
    ip = request.remote_addr
    names = glob('flaskr/' + ip + '/inbox/*', recursive=True)

    new_names = list()
    for name in names:
        name = name.replace('flaskr/' + ip + '/inbox/', '')
        if '_' in name:
            name = name[:name.index('_')]

        counter = {}
        if name in new_names:
            if name not in counter:
                counter['name'] = 2
            else:
                counter['name'] += 1
            name += f"_{counter['name']}"

        new_names.append(name)

    new_names.sort()
    names.sort()

    return {new_name: name for new_name, name in zip(new_names, names)}


class Conversation:
    """A class representing a conversation."""

    def __init__(self, df) -> None:
        self.df = dataframe.create_megaframe(df)

    def individual_messages_count(self) -> dict:
        """Return a dict where the keys are people and values are message count."""
        return dict(self.df['sender_name'].value_counts())

    def people(self) -> tuple:
        """Returns a tuple containing the people involved in this conversation."""
        return tuple(self.df['sender_name'].unique())

    def total_message_count(self) -> int:
        """Returns total messages sent in the conversation as an int"""
        return self.df['sender_name'].count()

    def common_words(self) -> list[tuple[str, int]]:
        """Returns the most common words after removing stopwords"""
        texts = self.df['content'].dropna()
        all_words = ''.join(texts).split()
        stop_words = set(stopwords.words('english'))
        filtered = [word for word in all_words if word.lower() not in stop_words]
        return Counter(filtered).most_common(10)

    def message_over_time(self, mode: str):
        """Returns an interactive graph showing cumulative messages over time."""
        idx = pd.date_range(
            start=self.df['timestamp_ms'].min().floor('d'),
            end=self.df['timestamp_ms'].max().floor('d')
        )

        series = (self.df['timestamp_ms']).dt.floor('d').value_counts()

        series.index = pd.DatetimeIndex(series.index)

        series = series.reindex(idx, fill_value=0)

        fig = series.plot(
            title='Amount of messages over time',
            labels={
                "value": "Cumulative messages count/day",
                "index": "Time"
            })

        if mode == 'flask':
            return fig
        elif mode == 'local':
            fig.show()
        else:
            raise KeyError

    def days_since_beginning(self):
        """Returns an int representing days since first text"""
        first_day = self.df['timestamp_ms'].min()
        today = pd.Timestamp.today()
        delta = today - first_day
        return delta.days

    def popular_hours(self, mode: str):
        """Returns a bar chart of most popular hours"""
        hour_count = self.df['timestamp_ms'].dt.hour.value_counts(
        ).sort_index()

        fig = hour_count.plot.bar(
            title='Most popular hours',
            labels={
                'value': 'Texts',
                'index': '24-hour time'
            }
        )

        fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=0
            )
        )

        if mode == 'flask':
            return fig
        elif mode == 'local':
            fig.show()
        else:
            raise KeyError

    def texted_first(self) -> str:
        """Returns the person that sent the first message"""
        return list(self.df['sender_name'])[-1]

    def first_text(self) -> str:
        """Returns the first messages sent"""
        return list(self.df['content'])[-1]

    def first_day(self) -> str:
        """Returns the first day of the text"""
        return str(list(self.df['timestamp_ms'])[-1].date())

    def convo_count(self):
        """
        Return the number of conversations (separated by 2-hour period)
        """
        time_list = list(self.df['timestamp_ms'])
        count = 0
        for i in range(len(time_list) - 1):
            if time_list[i] - time_list[i + 1] > datetime.timedelta(hours=2):
                count += 1
        return count

    def convo_initiators(self):
        sender_list = list(self.df['sender_name'])
        text_list = list(self.df['content'])
        time_list = list(self.df['timestamp_ms'])
        sender_list.reverse()
        text_list.reverse()
        time_list.reverse()
        initiators = {}
        for i in range(len(time_list) - 1):
            if time_list[i + 1] - time_list[i] > datetime.timedelta(hours=2):
                if sender_list[i + 1] not in initiators:
                    initiators[sender_list[i + 1]] = 1
                else:
                    initiators[sender_list[i + 1]] += 1

        return initiators

    def response_time(self):
        """
        Show distribution of response time
        """
        sender_list = list(self.df['sender_name'])
        time_list = list(self.df['timestamp_ms'])
        sender_list.reverse()
        time_list.reverse()
        response_time = {}

        for i in range(len(time_list) - 1):
            if sender_list[i + 1] not in response_time:
                response_time[sender_list[i + 1]] = [time_list[i + 1] - time_list[i]]
            else:
                response_time[sender_list[i + 1]].append([time_list[i + 1] - time_list[i]])

        return response_time

