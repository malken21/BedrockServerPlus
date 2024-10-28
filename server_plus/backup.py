import os
import zipfile
import datetime


# 色んな関数 インポート
import server_plus.util as util


from json import JSONEncoder

# 管理データのパス "save/backup.json" で 古すぎるファイルの削除を管理している
CONTROL_DATA_PATH = "./server_plus/save/backup.json"


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
def removeBackup(controlData: list, config):
    MaxBackupFile = config["MaxBackupFile"]

    # もし "MaxBackupFile" が 0 に設定されていた場合は return
    if MaxBackupFile == 0:
        return

    # 既に存在しないバックアップのデータを "controlData"から削除
    for i in controlData:
        if not os.path.isfile(i["path"]):
            controlData.remove(i)

    # 古すぎるバックアップファイル削除
    for i in range(len(controlData[MaxBackupFile:])):
        path = controlData[i + MaxBackupFile]["path"]
        os.remove(path)
        print("RemoveFile: " + path)

        # ウェブフック送信
        util.sendWebhook(
            {"type": "RemoveBackup", "path": os.path.abspath(path)}, config
        )

    # 削除されたバックアップファイルについてのデータを消す
    del controlData[MaxBackupFile:]

    return controlData


# ファイルバックアップ (zip)
def world(config):
    controlData = []
    # ./server_plus/save/backup.json (管理データ) が存在するかどうか
    if os.path.isfile(CONTROL_DATA_PATH):
        # 存在したら 書いているJSONを controlData に代入
        controlData = util.readJSON(CONTROL_DATA_PATH)

    # 現在の時間
    now = datetime.datetime.now()

    # ワールドのパス
    path = config["WorldPath"]
    # 作成するアーカイブファイルのパス
    ZipFilePath = now.strftime(config["WorldArchiveFile"])

    # 古すぎるバックアップファイルなどを削除
    controlData = removeBackup(controlData, config)

    controlData.insert(0, {"path": ZipFilePath, "time": now})

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

    # 変数"controlData"を保存
    util.saveJSON(CONTROL_DATA_PATH, controlData, cls=JSONEncoder_Datetime)
