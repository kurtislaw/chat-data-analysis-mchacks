"""
Overall
"""
import pandas as pd
from collections import Counter
from flaskr import dataframe
import os
from nltk.corpus import stopwords


def join_dataframe(inbox: str):
    """
    Iterate through conversation files,
    set up individual dataframe,
    and concatenate them
    """
    contacts = [f.path for f in os.scandir(inbox) if f.is_dir()]
    frames = []
    for contact in contacts:
        frames.append(dataframe.create_megaframe(contact))
    return pd.concat(frames)


class History:
    """
    Class representing entire chat history.
    """
    def __init__(self, df) -> None:
        self.df = join_dataframe(df)

    def individual_messages_count(self) -> dict:
        """Return a dict mapping people to message count."""
        return dict(self.df['sender_name'].value_counts())

    def total_message_count(self) -> int:
        """Returns total messages sent as an int"""
        return self.df['sender_name'].count()

    def people(self) -> tuple:
        """Returns a tuple containing the people messaged."""
        return tuple(self.df['sender_name'].unique())

    def total_message_count(self) -> int:
        """Returns total messages sent in the conversation as an int"""
        return self.df['sender_name'].count()

    def common_words(self):
        """Returns a dict with the most common words"""
        texts = self.df['content'].dropna()
        all_words = ''.join(texts).split()
        stop_words = set(stopwords.words('english'))
        filtered = [word for word in all_words if word.lower() not in stop_words]
        return Counter(filtered).most_common(20)

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
