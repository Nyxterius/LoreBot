import sqlite3 as sql

class requestHistory():
    def __init__(self):
        self.histDict = {}
        self.fields = list()
        self.countID = 1

    def store(self, game, topic, response, result):
        self.fields.append((f"**{game}: {topic}**", response, f"<{result}>"))
        self.histDict.update({self.countID : self.fields[0]})
        print(self.countID)
        self.countID += 1
        self.fields.pop(0)
        if len(self.histDict) > 30:
            self.histDict.clear()

    def returnHistory(self):
        return self.histDict.items()