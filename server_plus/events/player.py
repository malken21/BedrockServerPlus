from server_plus.events.default import event_webhook


class PlayerConnect(event_webhook):
    def run(self, text: str):
        # プレイヤー接続ログかどうか
        if text.startswith("Player connected: "):
            # ウェブフック
            self.sendWebhook(
                {"type": "PlayerConnect",
                    "username": __getPlayerName(text)}
            )


class PlayerDisconnect(event_webhook):
    def run(self, text: str):
        # プレイヤー切断ログかどうか
        if text.startswith("Player disconnected: "):
            # ウェブフック
            self.sendWebhook(
                {"type": "PlayerDisconnect",
                    "username": __getPlayerName(text)}
            )


# ログの本文からプレイヤー名の部分を取得する
def __getPlayerName(text: str):
    start = text.find(":") + 2
    end = text.find(",", start)
    username = text[start:end]
    return username
