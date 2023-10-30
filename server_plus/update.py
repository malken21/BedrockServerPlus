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

# def isLatest(ver:str):


def getVersionFromLog(log: str):
    v = re.search(LogSearch, log)
    if v is None or len(v.groups()) != 1:
        return
    global version
    version = v.group(1)

    print(version)


def tryUpdate():
    if os.path.isfile(saveDataPath):
        # 存在したら 書いているJSONを saveData に代入
        saveData = util.readJSON(saveDataPath)
