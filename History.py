class requestHistory():
    def __init__(self):
        self.histDict = {}

    def store(self, game, topic, result):
        self.histDict[f"{game} {topic}"] = f"{result}"
        print(self.histDict[f"{game} {topic}"])
        if len(self.histDict) > 6:
            self.histDict.clear()

    def returnHistory(self):
        counter = 0
        histList = []
        for i, j in self.histDict.items():
            counter += 1
            histList.append(str(counter) + f"\n **{i}** " + f"<{j}>" + "\n")
        return (', '.join(histList))