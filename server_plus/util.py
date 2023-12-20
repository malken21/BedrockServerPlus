from urllib import request, error
from threading import Thread
import os
import json
import yaml


# エスケープ UTF-16BE
def escape_utf16be(input_string):
    return "".join(["\\u{:04X}".format(ord(c)) for c in input_string])


# 読み込み JSON
def readJSON(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# 書き込み JSON
def saveJSON(path, data, cls=None):
    # パスまでのディレクトリが存在しない場合は作成
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False, cls=cls)


def getConfig():
    PATH = "server_plus/config.yml"

    config = readYAML("server_plus/default.yml")

    if os.path.exists(PATH):
        config.update(readYAML(PATH))

    return config


# 読み込み YAML
def readYAML(path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=yaml.Loader)


# config の ActionTimerList に書かれた実行内容をコマンドに変換
def toCommand(ActionTimer):
    if "command" in ActionTimer:
        command = ActionTimer["command"]
        if command.startswith("/"):
            return command[1:]
        else:
            return command

    elif "say" in ActionTimer:
        return 'tellraw @a {"rawtext": [{"text": "%s"}]}' % escape_utf16be(
            ActionTimer["say"]
        )


# リクエストボディに JSON が書かれている Post 送信
def postJSON(url: str, data):
    headers = {"Content-Type": "application/json"}
    data = json.dumps(data)
    data = data.encode("utf-8")

    try:
        req = request.Request(url, data, headers)
        with request.urlopen(req) as response:
            response_text = response.read().decode("utf-8")
            return response_text
    except error.URLError:
        return None


# 終了処理
def exit():
    os._exit(1)


# 型か文字列かどうか
def is_str(v):
    return type(v) is str


# Webhook 送信
def sendWebhook(data, config):
    # config で Webhookの機能が 無効だったら return
    if config["Webhook"] == False:
        return

    # スレッドを作成、開始 Postリクエストを送信
    thread = Thread(target=postJSON, args=(config["WebhookURL"], data))
    thread.start()


# スレッドを作成せずに Webhook 送信
def sendWebhookAwait(data, config):
    # config で Webhookの機能が 無効だったら return
    if config["Webhook"] == False:
        return

    # Postリクエストを送信
    postJSON(config["WebhookURL"], data)


# Webページの情報を取得する (リダイレクトに対応)
def fetch_data(url: str, headers={}):
    try:
        # リダイレクトを自動的に処理するOpenerを作成
        opener = request.build_opener(
            request.HTTPCookieProcessor())
        request.install_opener(opener)

        # GETリクエストを送信し、レスポンスを取得
        req = request.Request(url, headers=headers)
        # レスポンスの内容（HTMLなど）を取得
        res = opener.open(req)
        return res.read()
    except (error.HTTPError, error.URLError):
        return None
