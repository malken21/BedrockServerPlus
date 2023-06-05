# BedrockServerPlus

 統合版の実績解除が可能なサーバーにログインメッセージや時報などを設定できるようにする

## Webhook の機能 について

config.yml で指定した URL に Post でリクエストを送信する

以下は リクエストが送信される条件と リクエストした時の リクエストボディ について

リクエストボディは JSON です

### サーバー起動時

```post
{"type": "ServerStart"}
```

### サーバー停止時

```post
{"type": "ServerStop"}
```

### プレイヤー接続時

```post
{"type": "PlayerConnect", "username": "ユーザー名"}
```

### プレイヤー切断時

```post
{"type": "PlayerDisconnect", "username": "ユーザー名"}
```

### ワールドバックアップ作成時

```post
{"type": "CreateBackup", "path": "バックアップファイルの絶対パス"}
```

### ワールドバックアップ削除時

```post
{"type": "RemoveBackup", "path": "バックアップファイルの絶対パス"}
```
