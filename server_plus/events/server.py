from server_plus.events.default import event_webhook


class event_server(event_webhook):
    def __init__(self, config, weather):
        super().__init__(config)
        self.weather = weather


class ServerStart(event_server):
    def run(self, text: str):
        # サーバー 起動ログだったら
        if text == "Server started.":
            self.weather.isRunning = True
            self.sendWebhook({"type": "ServerStart"})


class ServerStop(event_server):
    def run(self, text: str):
        # サーバー 停止ログだったら
        if text == "Stopping server...":
            self.weather.isRunning = False
            self.sendWebhook({"type": "ServerStop"})
