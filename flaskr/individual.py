"""
Individuals
"""
import pandas as pd
from flaskr import dataframe
import plotly.io as pio
from glob import glob
from collections import Counter

pio.renderers.default = "browser"
pd.options.plotting.backend = 'plotly'


def find_all_names() -> dict:
    """Parses through inbox directory, returns the names of all people."""
    names = glob('./inbox/*', recursive=True)

    new_names = list()
    for name in names:
        name = name.replace('./inbox/', '')
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

    def common_words(self):
        """Returns a dict with the most common words"""
        texts = self.df['content'].dropna()

        return Counter(''.join(texts).split()).most_common(10)

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
