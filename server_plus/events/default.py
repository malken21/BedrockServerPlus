import server_plus.util as util


class event:
    def __init__(self, config):
        self.config = config

    def setLogOutput(self, value: bool):
        self.__LogOutput = value

    def isLogOutput(self) -> bool:
        return self.__LogOutput

    def run(self, text: str):
        pass


class event_webhook(event):
    def sendWebhook(self, data):
        util.sendWebhook(
            data, self.config
        )
        print(f"sendWebhook: {data}")
