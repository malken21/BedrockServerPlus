from threading import Thread
import asyncio

from server_plus.events.default import event_webhook

import server_plus.process as process


class WeatherUpdate(event_webhook):

    def __init__(self, config, server: process.server):
        super().__init__(config)
        self.server = server
        self.__isSendCommand = False
        # 統合版サーバー メインの処理 起動
        Thread(target=self.loop).start()

    async def loop(self):
        self.SendCommand()
        await asyncio.sleep(10)

    def run(self, text: str):

        # 天候を取得したログかどうか
        if self.__isSendCommand and text.startswith("Weather state is: "):
            self.__isSendCommand = False
            # ウェブフック
            self.sendWebhook(
                {"type": "WeatherUpdate",
                    "name": __getWeatherName(text)}
            )
            self.setLogOutput(False)

    def SendCommand(self):
        self.server.write_text("weather query")
        self.__isSendCommand = True


# ログの本文から天候名の部分を取得する
def __getWeatherName(text: str):
    start = text.find(":") + 2
    name = text[start:]
    return name
