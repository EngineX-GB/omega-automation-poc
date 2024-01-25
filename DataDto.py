class DataDto:

    def __init__(self, link, outputFileName, strategyMode):
        self.link = link
        self.outputFileName = outputFileName
        self.strategyMode = strategyMode

    def getLink(self):
        return self.link

    def getOutputFileName(self):
        return self.outputFileName

    def getStrategyMode(self):
        return self.strategyMode

    def getRecord(self):
        return ((self.outputFileName + "|" + self.strategyMode + "|" + self.link))