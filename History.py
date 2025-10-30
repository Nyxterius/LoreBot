class requestHistory():
    def __init__(self):
        self.histDict = {}

    def store(self, game, topic, response, result):
        self.histDict[f"{game} {topic}"] = f"{result}\n{response}"
        if len(self.histDict) > 6:
            self.histDict.clear()

    def returnHistory(self):
        counter = 0
        for i, j in self.histDict:
            counter += 1
            print(f"{counter} entries.")
            print(i, j)
            return (str(counter) + i + j)