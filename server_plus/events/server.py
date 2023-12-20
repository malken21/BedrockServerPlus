from server_plus.eventManager import event
from server_plus.util import sendWebhook


class ServerStart(event):
    def run(self, text: str):
        # サーバー 起動ログだったら
        if text == "Server started.":
            sendWebhook({"type": "ServerStart"}, self.config)


class ServerStop(event):
    def run(self, text: str):
        # サーバー 停止ログだったら
        if text == "Stopping server...":
            sendWebhook({"type": "ServerStop"}, self.config)
