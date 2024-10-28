from subprocess import PIPE, Popen

# 色んな関数 インポート
import server_plus.util as util

# バックアップ関係
import server_plus.backup as backup

import server_plus.log as log
from server_plus.eventRegister import EventList

from server_plus.update import check


# サブプロセス (統合版サーバー) 作成
def ServerStart(config):
    check()  # アップデート確認
    return Popen(  # サーバー起動
        config["startCMD"],
        stdin=PIPE,
        stdout=PIPE,
        shell=True,
        encoding="utf-8",
        universal_newlines=True,
    )


class server:

    def __init__(self, bedrock: Popen, config):
        self.bedrock = bedrock
        self.config = config
        self.events = EventList(config, self).get()
        # 現在の状態を管理
        self.status = {"isReboot": False}

    # メインの処理
    def main(self):
        while True:
            poll = self.bedrock.poll()
            if poll is None:
                # 出力された文字読み込み
                output: str = self.bedrock.stdout.readline()
                output.strip()

                # ログを取得した時の処理
                log.getLog(output, self.events)

            elif poll == 0:
                if self.config["Backup"]:
                    # バックアップ
                    backup.world(self.config)

                if self.status["isReboot"]:
                    # 再起動
                    self.status["isReboot"] = False
                    # 統合版サーバー プロセス起動
                    self.bedrock = ServerStart(self.config)
                else:
                    util.exit()
            else:
                util.exit()

    # コンソールから読み取り
    def read_input(self):
        while True:
            user_input = input()
            if self.bedrock.poll() is None:
                if user_input == "reboot":
                    self.status["isReboot"] = True
                    self.write_text("stop")

                self.write_text(user_input)

    # 文字 (引数 text) を書き込み
    def write_text(self, text: str):
        self.bedrock.stdin.write(text + "\n")
        self.bedrock.stdin.flush()
