
import os
import zipfile
import datetime
import time


# 色んな関数 インポート
import server_plus.util as util


from json import JSONEncoder

# 保存データのパス
saveDataPath = "./server_plus/save/backup.json"


class JSONEncoder_Datetime(JSONEncoder):  # JSONEncoderを継承させる

    def default(self, o):
        if type(o).__name__ == "datetime":     # 値がdatetime型だったら、
            return o.strftime("%Y%m%d-%H%M%S")  # 文字列に変換して返す
        else:
            return o


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
    zipFile_Name = now.strftime(config["WorldArchiveFile"])

    saveData.append({
        "path": zipFile_Name,
        "time": now
    })

    saveData = normalization(saveData)

    # アーカイブファイル作成
    with zipfile.ZipFile(zipFile_Name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(path, zipf)

    # 変数"saveData"を保存
    util.saveJSON(saveDataPath, saveData, cls=JSONEncoder_Datetime)


def zipdir(path, ziph):
    # zipfileハンドル
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path)
            )


# "saveData" にある "time" にある文字列を"datetime"に変換し
# 変換し終わったものを return する
def normalization(saveData):
    for i in range(len(saveData)):
        time = saveData[i]["time"]
        # もし型が 文字列 の場合は "datetime"に変換する
        if (util.is_str(time)):
            time = datetime.datetime.strptime(time, "%Y%m%d-%H%M%S")
            saveData[i]["time"] = time
    return saveData
