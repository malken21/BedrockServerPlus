import subprocess
from subprocess import PIPE

# 色んな関数 インポート
import server_plus.util as util

# バックアップ関係
import server_plus.backup as backup

import server_plus.log as log

# config.json 読み込み
config = util.readYAML("server_plus/config.yml")

# config に書いてある 統合版サーバー 起動コマンド を "startCMD" に代入
startCMD = config["startCMD"]


# サブプロセス (統合版サーバー) 作成
def ServerStart():
    util.sendWebhook({"type": "ServerStart"}, config)
    return subprocess.Popen(
        startCMD,
        stdin=PIPE,
        stdout=PIPE,
        shell=True,
        encoding="utf-8",
        universal_newlines=True,
    )


# 統合版サーバー プロセス起動
process = ServerStart()
# 現在の状態を管理
status = {"isReboot": False}


# メインの処理
def main():
    global process, status
    while True:
        poll = process.poll()
        if poll is None:
            # 出力された文字読み込み
            output = process.stdout.readline().strip()

            # ログを取得した時の処理
            log.getLog(output, config)

        elif poll == 0:
            util.sendWebhook({"type": "ServerStop"}, config)
            if config["Backup"]:
                # バックアップ
                backup.world(config)

            if status["isReboot"]:
                # 再起動
                status["isReboot"] = False
                # 統合版サーバー プロセス起動
                process = ServerStart()
            else:
                util.exit()
        else:
            util.exit()


# コンソールから読み取り
def read_input():
    global process
    while True:
        user_input = input()
        if process.poll() is None:
            write_text(user_input + "\n")


# 文字 (引数 text) を書き込み
def write_text(text: str):
    global process
    process.stdin.write(text)
    process.stdin.flush()
