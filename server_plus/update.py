import zipfile
import os


def unzip_exclude(zip_filepath, extract_dir, exclude_files):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if member not in exclude_files:
                zip_ref.extract(member, extract_dir)


EXTRACT_DIR = '.'  # 解凍先のディレクトリ
EXCLUDE_FILES = [
    'server.properties',
    'permissions.json',
    'allowlist.json'
]  # 除外したいファイルのリスト


def getZipPath(path: str, search_string=""):
    for file in os.listdir(path):
        if file.endswith('.zip') and search_string in file:
            return os.path.join(path, file)
    # 該当するファイルが見つからなかった場合
    return None


ZIP_FILE_PATH = getZipPath(".", "bedrock-server")

print(ZIP_FILE_PATH)

if ZIP_FILE_PATH is not None:
    unzip_exclude(ZIP_FILE_PATH, EXTRACT_DIR, EXCLUDE_FILES)
