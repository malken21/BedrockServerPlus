
import os
import zipfile
import datetime

# 色んな関数 インポート
import server_plus.util as util

# ファイルバックアップ (zip)


def world(config):

    now = datetime.datetime.now()

    path = config["WorldPath"]
    zipFile_Name = now.strftime(config["WorldArchiveName"])

    zipf = zipfile.ZipFile(zipFile_Name, 'w', zipfile.ZIP_DEFLATED)
    zipdir(path, zipf)
    zipf.close()


def zipdir(path, ziph):
    # zipfileハンドル
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file),
                os.path.relpath(os.path.join(root, file), path)
            )
