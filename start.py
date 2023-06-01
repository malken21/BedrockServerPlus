import threading
import subprocess
from subprocess import PIPE
import asyncio

# プロセス関係 読み込み (統合版サーバーとの接続)
from server_plus.process import print_output,  read_input, write_text

# その他色んな関数 インポート
import server_plus.util as util

# config.json 読み込み
config = util.readJSON("server_plus/config.json")

# config に書いてある 統合版サーバー 起動コマンド を "startCMD" に代入
startCMD = config["startCMD"]


def ServerStart():
    # サブプロセス (統合版サーバー) 作成
    process = subprocess.Popen(startCMD, stdin=PIPE, stdout=PIPE, shell=True)

    # コンソールに "統合版サーバーのコンソール" を表示する
    output = threading.Thread(target=print_output, args=(process,))
    output.start()

    # コンソールからコマンドの実行をできるようにする

    loop = asyncio.get_event_loop()
    loop.call_soon(read_input, process)
    loop.run_forever()

    # "統合版サーバーのコンソール"の出力が止まるまで (サーバーが停止するまで)
    # ここで一時停止する
    output.join()
    #


ServerStart()

print("logkjpe")
