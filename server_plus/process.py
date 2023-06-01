
import subprocess
from subprocess import PIPE

# その他色んな関数 インポート
import server_plus.util as util

# config.json 読み込み
config = util.readJSON("server_plus/config.json")

# config に書いてある 統合版サーバー 起動コマンド を "startCMD" に代入
startCMD = config["startCMD"]


# サブプロセス (統合版サーバー) 作成
def ServerStart():
    return subprocess.Popen(startCMD, stdin=PIPE, stdout=PIPE, shell=True)


# 統合版サーバー プロセス起動
process = ServerStart()


# メインの処理
def main():
    global process
    while True:
        if process.poll() is None:
            # 出力された文字読み込み
            output = process.stdout.readline()
            # コンソール出力
            print(output.strip().decode())
        else:
            process = ServerStart()


# コンソールから読み取り
def read_input():
    global process
    while True:
        user_input = input()
        if (process.poll() is None):
            write_text(user_input + "\n")


# 文字 (引数 text) を書き込み
def write_text(text: str):
    global process
    process.stdin.write(text.encode())
    process.stdin.flush()
