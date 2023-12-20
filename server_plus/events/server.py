from server_plus.events.default import event_webhook


class ServerStart(event_webhook):
    def run(self, text: str):
        # サーバー 起動ログだったら
        if text == "Server started.":
            self.sendWebhook({"type": "ServerStart"})


class ServerStop(event_webhook):
    def run(self, text: str):
        # サーバー 停止ログだったら
        if text == "Stopping server...":
            self.sendWebhook({"type": "ServerStop"})
