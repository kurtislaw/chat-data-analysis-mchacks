"""
Analyze a given conversation. Calculate statistics and trends.
"""


class Analyze():

    def __init__(self, messages, participants) -> None:
        self.messages = messages
        self.recipiant = participants[0]['name']
        self.user = participants[1]['name']

    def recipiant_name(self):
        return self.recipiant

##########################################################
#   STATISTICS
##########################################################

    def total_messages(self):
        """
        Return the total number of messages sent by a person
        """
        return sum(message['name'] == self.user for message in self.messages)

    def common_words(self):
        """
        Return the common words in the conversation
        """
        words = {}

        for m in self.messages:
            for word in m['content'].split():
                if word not in words:
                    words[word] = 1
                else:
                    words[word] += 1

        return [words.keys()][:5]
