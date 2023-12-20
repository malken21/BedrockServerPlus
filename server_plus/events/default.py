class event:
    def __init__(self, config):
        self.config = config

    def setLogOutput(self, value: bool):
        self.__LogOutput = value

    def isLogOutput(self) -> bool:
        return self.__LogOutput

    def run(self, text: str):
        pass
