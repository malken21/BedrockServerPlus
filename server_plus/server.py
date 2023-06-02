import threading
import asyncio
import schedule

# プロセス関係 読み込み (統合版サーバーとの接続)
from server_plus.process import status, config, main,  read_input, write_text

import server_plus.util as util


def run():

    # 統合版サーバー メインの処理 起動
    output = threading.Thread(target=main, args=())
    output.start()

    # コンソールからコマンドの実行をできるようにする
    input = threading.Thread(target=read_input, args=())
    input.start()

    # 自動再起動の設定
    if (config["Reboot"]):
        RebootTime = config["RebootTime"]
        print("RebootTime: " + RebootTime)
        schedule.every().day.at(RebootTime).do(reboot)

    # 自動コマンド実行の登録
    if (config["ActionTimer"]):
        CommandTimerList = config["ActionTimerList"]

        for item in CommandTimerList:
            time = item["time"]
            schedule.every().day.at(time).do(
                write_text,
                text=util.toCommand(item) + "\n"
            )

    # 常時実行
    asyncio.run(loop())


# 常時実行
async def loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


# 再起動
def reboot():
    status["isReboot"] = True
    write_text("stop\n")
