class requestHistory():
    def __init__(self):
        self.histDict = {}
        self.fields = list()
        self.countID = 1

    def store(self, game, topic, response, result):
        self.histDict[f"{game} {topic}"] = f"{result}\n{response}"
        if len(self.histDict) > 6:
            self.histDict.clear()
            self.countID = 1

    def returnHistory(self):
        counter = 0
        for i, j in self.histDict:
            counter += 1
            return (str(counter) + i + j)