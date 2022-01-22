"""
Individuals
"""
import pandas as pd

import dataframe
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"


class Conversation:
    """
    A class representing a conversation.
    """
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
        sentences = list(self.df['content'])
        words = []
        for sentence in sentences:
            for word in sentence.split():
                words.append(word)
        return words

    def message_over_time(self):
        """Returns an interactive graph showing cumulative messages over time."""
        idx = pd.date_range(
            start=self.df['timestamp_ms'].min().floor('d'),
            end=self.df['timestamp_ms'].max().floor('d')
            )

        series = (self.df['timestamp_ms']).dt.floor('d').value_counts()

        series.index = pd.DatetimeIndex(series.index)

        series = series.reindex(idx, fill_value=0)

        pd.options.plotting.backend = 'plotly'

        fig = series.plot(
            title='Amount of messages over time',
                              labels={
                                  "value": "Cumulative messages count/day",
                                  "index": "Time"
                              })
        fig.show()


