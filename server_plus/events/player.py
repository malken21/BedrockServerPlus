from server_plus.eventManager import event
from server_plus.util import sendWebhook


class PlayerConnect(event):
    def run(self, text: str):
        # プレイヤー接続ログかどうか
        if text.startswith("Player connected: "):
            # ウェブフック
            sendWebhook(
                {"type": "PlayerConnect",
                    "username": __getPlayerName(text)}, self.config
            )


class PlayerDisconnect(event):
    def run(self, text: str):
        # プレイヤー切断ログかどうか
        if text.startswith("Player disconnected: "):
            # ウェブフック
            sendWebhook(
                {"type": "PlayerDisconnect",
                    "username": __getPlayerName(text)}, self.config
            )


# ログの本文からプレイヤー名の部分を取得する
def __getPlayerName(text: str):
    start = text.find(":") + 2
    end = text.find(",", start)
    username = text[start:end]
    return username
