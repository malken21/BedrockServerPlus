from server_plus.eventManager import event
from server_plus.util import sendWebhook


class WeatherUpdate(event):
    def run(self, text: str):
        # プレイヤー切断ログかどうか
        if text.startswith("Weather state is: "):
            # ウェブフック
            sendWebhook(
                {
                    "type": "WeatherUpdate",
                    "name": __getWeatherName(text)
                }, self.config
            )
            self.setLogOutput(False)


# ログの本文から天候名の部分を取得する
def __getWeatherName(text: str):
    start = text.find(":") + 2
    name = text[start:]
    return name
