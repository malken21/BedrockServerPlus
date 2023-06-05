# BedrockServerPlus

 統合版の実績解除が可能なサーバーにログインメッセージや時報などを設定できるようにする

## Webhook の機能 について

config.yml で指定した URL に Post でリクエストを送信する

### サーバー起動時

リクエストボディ

```post
{}
```
