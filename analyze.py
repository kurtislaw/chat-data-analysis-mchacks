"""
Analyze a given conversation. Calculate statistics and trends.
"""


class Megaframe:

    def __init__(self, messages, participants) -> None:
        self.messages = messages
        self.recipient = participants[0]['name']
        self.user = participants[1]['name']

    def recipient_name(self):
        return self.recipient

##########################################################
#   STATISTICS
##########################################################

    def total_messages(self):
        return sum(message['name'] == self.user for message in self.messages)

    def common_words(self):
        words = {}

        for m in self.messages:
            for word in m['content'].split():
                if word not in words:
                    words[word] = 1
                else:
                    words[word] += 1

        return [words.keys()][:5]
