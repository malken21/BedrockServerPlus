import os
import json
import yaml


# エスケープ UTF-16BE
def escape_utf16be(input_string):
    return ''.join(['\\u{:04X}'.format(ord(c)) for c in input_string])


# 読み込み JSON
def readJSON(path):
    with open(path, 'r', encoding="utf-8") as file:
        return json.load(file)


# 書き込み JSON
def saveJSON(path, data, cls=None):

    # パスまでのディレクトリが存在しない場合は作成
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False, cls=cls)


# 読み込み YAML
def readYAML(path):
    with open(path, 'r', encoding="utf-8") as file:
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
        return 'tellraw @a {"rawtext": [{"text": "%s"}]}' % escape_utf16be(ActionTimer["say"])


# 終了処理
def exit():
    os._exit(1)

# 型か文字列かどうか
def is_str(v):
    return type(v) is str