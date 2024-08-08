class requestHistory():
    def __init__(self):
        self.histDict = {}
        self.fields = list()
        self.countID = 1

    def store(self, game, topic, response, result):
        self.fields.append((f"**{game}: {topic}**", response, f"<{result}>"))
        self.histDict.update({self.countID : self.fields[0]})
        print(f"{self.countID} entries.")
        self.countID += 1
        self.fields.pop(0)
        if len(self.histDict) > 6:
            self.histDict.clear()
            self.countID = 1

    def returnHistory(self):
        return self.histDict.items()