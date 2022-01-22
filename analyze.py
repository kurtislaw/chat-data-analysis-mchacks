"""
Analyze a given conversation. Calculate statistics and trends.
"""

class Analyze():

    def __init__(self, messages, participants) -> None:
        self.MESSAGES = messages
        self.recipiant = participants[0]['name']
    
    def get_recipiant_name():
        return self.recipiant