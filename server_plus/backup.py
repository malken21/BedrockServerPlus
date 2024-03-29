import os
import zipfile
import datetime


# 色んな関数 インポート
import server_plus.util as util


from json import JSONEncoder

# 保存データのパス "save/backup.json" で 古すぎるファイルの削除を管理している
saveDataPath = "./server_plus/save/backup.json"


class JSONEncoder_Datetime(JSONEncoder):  # JSONEncoderを継承させる
    def default(self, o):
        if type(o).__name__ == "datetime":  # 値がdatetime型だったら、
            return o.strftime("%Y%m%d-%H%M%S")  # 文字列に変換して返す
        else:
            return o


def zipdir(path, ziph):
    # zipfileハンドル
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path),
            )


# ファイルのパスまでのディレクトリがない場合作成する
def createDir(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


# 古いバックアップを削除
def removeBackup(saveData: list, config):
    MaxBackupFile = config["MaxBackupFile"]

    # もし "MaxBackupFile" が 0 に設定されていた場合は return
    if MaxBackupFile == 0:
        return

    # 既に存在しないバックアップのデータを "saveData"から削除
    for i in saveData:
        if not os.path.isfile(i["path"]):
            saveData.remove(i)

    # 古すぎるバックアップファイル削除
    for i in range(len(saveData[MaxBackupFile:])):
        path = saveData[i + MaxBackupFile]["path"]
        os.remove(path)
        print("RemoveFile: " + path)

        # ウェブフック送信
        util.sendWebhook(
            {"type": "RemoveBackup", "path": os.path.abspath(path)}, config
        )

    # 削除されたバックアップファイルについてのデータを消す
    del saveData[MaxBackupFile:]

    return saveData


# ファイルバックアップ (zip)
def world(config):
    saveData = []
    # ./server_plus/save/backup.json (保存データ) が存在するかどうか
    if os.path.isfile(saveDataPath):
        # 存在したら 書いているJSONを saveData に代入
        saveData = util.readJSON(saveDataPath)

    # 現在の時間
    now = datetime.datetime.now()

    # ワールドのパス
    path = config["WorldPath"]
    # 作成するアーカイブファイルのパス
    ZipFilePath = now.strftime(config["WorldArchiveFile"])

    # 古すぎるバックアップファイルなどを削除
    saveData = removeBackup(saveData, config)

    saveData.insert(0, {"path": ZipFilePath, "time": now})

    # バックアップファイルが作成されるディレクトリがない場合作成する
    createDir(ZipFilePath)

    # アーカイブファイル作成
    with zipfile.ZipFile(ZipFilePath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        zipdir(path, zipf)

    print("CreateFile: " + ZipFilePath)

    # ウェブフック送信
    util.sendWebhookAwait(
        {"type": "CreateBackup", "path": os.path.abspath(ZipFilePath)}, config
    )

    # 変数"saveData"を保存
    util.saveJSON(saveDataPath, saveData, cls=JSONEncoder_Datetime)
