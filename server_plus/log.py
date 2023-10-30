# 色んな関数 インポート
import server_plus.util as util


# 統合版サーバーのログを取得した時に実行される
def getLog(log, config):

    if log == "":
        return

    # コンソール出力
    print(log)

    # ログから本文を取得
    text = util.getMainText(log)

    # もし本文が取得できない場合は return
    if text is None:
        return

    # プレイヤー接続ログかどうか
    if text.startswith("Player connected: "):
        # ウェブフック
        util.sendWebhook(
            {"type": "PlayerConnect",
                "username": util.getPlayerName(text)}, config
        )

    # プレイヤー切断ログかどうか
    elif text.startswith("Player disconnected: "):
        # ウェブフック
        util.sendWebhook(
            {"type": "PlayerDisconnect",
                "username": util.getPlayerName(text)}, config
        )
    # サーバー 起動ログだったら
    elif text == "Server started.":
        util.sendWebhook({"type": "ServerStart"}, config)
    # サーバー 停止ログだったら
    elif text == "Stopping server...":
        util.sendWebhook({"type": "ServerStop"}, config)
