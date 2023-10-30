import os
import zipfile
import re


# 色んな関数 インポート
import server_plus.util as util

# 保存データのパス "save/update.json" で 古すぎるファイルの削除を管理している
saveDataPath = "./server_plus/save/update.json"

saveData = {}

LogSearch = r"\[*\] Version (.*)"

version = None

# config.json 読み込み
config = util.readYAML("server_plus/config.yml")



# サーバーのログからバージョンを取得して
# 最新版と違う場合は更新する
def getVersionFromLog(log: str):
    this_ver = re.search(LogSearch, log)
    if this_ver is None or len(this_ver.groups()) != 1:
        return
    global version
    version = this_ver.group(1)
    print("This version: %s" % (version))


def tryUpdate():
    if os.path.isfile(saveDataPath):
        # 存在したら 書いているJSONを saveData に代入
        saveData = util.readJSON(saveDataPath)
