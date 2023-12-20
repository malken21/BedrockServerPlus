import re
import server_plus.eventManager as eventManager


# 統合版サーバーのログを取得した時に実行される
def getLog(log: str, events: list[eventManager.event]):

    # ログから本文を取得
    text = __getMainText(log)

    # もし本文が取得できたら
    if text is not None:
        if eventManager.run(events, text):
            # コンソール出力
            print(log)


# ログから 本文を取得する 所得出来ない場合は None を返す
def __getMainText(log: str):

    if log != "":
        match = re.search(r"\[.*]\s(.*)", log)
        if match:
            return match.group(1)

    return None
