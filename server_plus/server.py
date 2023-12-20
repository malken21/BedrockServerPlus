from threading import Thread
import asyncio
import schedule
import server_plus.util as util

# プロセス関係 読み込み (統合版サーバーとの接続)
import server_plus.process as process


# config.json 読み込み
config = util.getConfig()
# config に書いてある 統合版サーバー 起動コマンド を "startCMD" に代入
# 統合版サーバー プロセス起動
bedrock = process.ServerStart(config)

server = process.server(bedrock, config)


def run():
    # 統合版サーバー メインの処理 起動
    output = Thread(target=server.main)
    output.start()

    # コンソールからコマンドの実行をできるようにする
    input = Thread(target=server.read_input)
    input.start()

    # 自動再起動の設定
    if config["Reboot"]:
        RebootTime = config["RebootTime"]
        print("RebootTime: " + RebootTime)
        schedule.every().day.at(RebootTime).do(reboot)

    # 自動コマンド実行の登録
    if config["ActionTimer"]:
        ActionTimerList = config["ActionTimerList"]

        for item in ActionTimerList:
            Time = item["time"]
            Command = util.toCommand(item)
            schedule.every().day.at(Time).do(server.write_text, text=Command)
            print(item)

    # 常時実行
    asyncio.run(loop())


# 常時実行
async def loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


# 再起動
def reboot():
    server.status["isReboot"] = True
    server.write_text("stop")
