import threading
import asyncio

# プロセス関係 読み込み (統合版サーバーとの接続)
from server_plus.process import status, main,  read_input, write_text


def run():

    # 統合版サーバー メインの処理 起動
    output = threading.Thread(target=main, args=())
    output.start()

    # コンソールからコマンドの実行をできるようにする
    input = threading.Thread(target=read_input, args=())
    input.start()

    # 常時実行
    asyncio.run(loop())


async def loop():
    while True:
        await asyncio.sleep(1)
        print("test")


# 再起動
def reboot():
    status["isReboot"] = False
    write_text("stop")
