import zipfile
import os
from html.parser import HTMLParser
import shutil

import server_plus.util as util


# 管理データのパス "save/update.json" で 現在のバージョンを管理している
CONTROL_DATA_PATH = "./server_plus/save/update.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
ZIP_FILE_PATH = "./tmp/bedrock_server.zip"
EXTRACT_DIR = '.'  # 解凍先のディレクトリ
EXCLUDE_FILES = [
    'server.properties',
    'permissions.json',
    'allowlist.json'
]  # 除外したいファイルのリスト


def unzip_exclude(zip_filepath, extract_dir, exclude_files):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if member not in exclude_files:
                zip_ref.extract(member, extract_dir)


def getZipPath(path: str, search_string=""):
    for file in os.listdir(path):
        if file.endswith('.zip') and search_string in file:
            return os.path.join(path, file)
    # 該当するファイルが見つからなかった場合
    return None


# Minecraft 公式サイトから zipファイル取得
def getZipDict():
    class getZipParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.zip_dict = {}

        def handle_starttag(self, tag, attrs):
            # a タグじゃなかったら return
            if tag != 'a':
                return
            # HTMLタグの情報を 辞書型に変換
            attrs_dict = dict(attrs)
            # もし 統合版サーバーの zipファイル が書かれてない場合は return
            if not attrs_dict.get('href', '').startswith('https://www.minecraft.net/bedrockdedicatedserver/'):
                return
            zip_url = attrs_dict['href']

            if "/bin-win/" in zip_url:  # Windows用のzipファイルだったら
                self.zip_dict["bin-win"] = zip_url
            elif "/bin-win-preview/" in zip_url:  # Windows用のプレビュー版zipファイルだったら
                self.zip_dict["bin-win-preview"] = zip_url
            elif "/bin-linux/" in zip_url:  # Linux用のzipファイルだったら
                self.zip_dict["bin-linux"] = zip_url
            elif "/bin-linux-preview/" in zip_url:  # Linux用のプレビュー版zipファイル だったら
                self.zip_dict["bin-linux-preview"] = zip_url

    # Minecraft 統合版サーバー 公式ダウンロードサイト
    URL = "https://minecraft.net/en-us/download/server/bedrock"
    response = util.fetch_data(URL, HEADERS)
    # HTMLをパース
    parser = getZipParser()
    parser.feed(response.decode('utf-8'))
    return parser.zip_dict


def upgrade(zip_url: str):
    dir_path = os.path.dirname(ZIP_FILE_PATH)
    os.makedirs(dir_path, exist_ok=True)  # zipファイルが一時的に保存されるディレクトリ作成
    util.download(zip_url, ZIP_FILE_PATH, HEADERS)  # zipファイルをダウンロード
    unzip_exclude(ZIP_FILE_PATH, EXTRACT_DIR, EXCLUDE_FILES)  # zipファイルを展開
    shutil.rmtree(dir_path)  # zipファイルが一時的に保存されていたディレクトリ削除


# アップデート確認
def check():
    controlData = {}
    # ./server_plus/save/backup.json (保存データ) が存在するかどうか
    if os.path.isfile(CONTROL_DATA_PATH):
        # 存在したら 書いているJSONを controlData に代入
        controlData = util.readJSON(CONTROL_DATA_PATH)

    bedrock_zip_dict = getZipDict()
    zip_url = None
    if os.name == "nt":  # Windows OS だったら
        if "bin-win" in bedrock_zip_dict:
            zip_url = bedrock_zip_dict["bin-win"]
    else:  # それ以外だったら
        if "bin-linux" in bedrock_zip_dict:
            zip_url = bedrock_zip_dict["bin-linux"]
    if "localZipURL" in controlData.items() and zip_url is controlData["localZipURL"]:
        return

    # 統合版サーバー アップグレード
    upgrade(zip_url)
    controlData["localZipURL"] = zip_url
    # 変数"controlData"を保存
    util.saveJSON(CONTROL_DATA_PATH, controlData)
