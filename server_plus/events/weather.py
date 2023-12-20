from threading import Thread
import time

from server_plus.events.default import event_webhook


class WeatherUpdate(event_webhook):

    def __init__(self, config, server):
        super().__init__(config)
        self.server = server
        self.__isSendCommand = False
        self.__old_weather = None
        # 統合版サーバー メインの処理 起動
        Thread(target=self.loop).start()

    def loop(self):
        self.SendCommand()
        time.sleep(10)
        self.loop()

    def run(self, text: str):

        # 天候を取得したログかどうか
        if self.__isSendCommand and text.startswith("Weather state is: "):
            self.__isSendCommand = False
            now_weather = _getWeatherName(text)
            self.setLogOutput(False)

            if self.isWeatherUpdate(now_weather):
                # ウェブフック
                self.sendWebhook(
                    {"type": "WeatherUpdate",
                        "name": now_weather}
                )

    def SendCommand(self):
        self.server.write_text("weather query")
        self.__isSendCommand = True

    def isWeatherUpdate(self, now_weather: str) -> bool:

        if self.__old_weather is None:
            self.__old_weather = now_weather

        elif self.__old_weather != now_weather:
            self.__old_weather = now_weather
            return True

        return False


# ログの本文から天候名の部分を取得する
def _getWeatherName(text: str):
    start = text.find(":") + 2
    name = text[start:]
    return name
