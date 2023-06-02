import json
import yaml


# 読み込み JSON
def readJSON(path):
    with open(path, 'r', encoding="utf-8") as file:
        return json.load(file)


# 書き込み JSON
def saveJSON(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 読み込み YAML
def readYAML(path):
    with open(path, 'r', encoding="utf-8") as file:
        return yaml.load(file)


# 書き込み YAML
def saveYAML(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, indent=4, ensure_ascii=False)
