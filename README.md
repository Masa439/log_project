# Flask ログ管理 API

このプロジェクトは Flask + SQLite を使用してログデータを管理する API です。
ログの取得・追加・検索・フィルタリング機能を提供します。

---

## プロジェクト概要

| 項目      | 内容                                   |
| ------- | ------------------------------------ |
| 言語      | Python 3.9                           |
| フレームワーク | Flask                                |
| データベース  | SQLite                               |
| 認証      | なし（開発用）                              |
| ホスティング  | ローカル（AWSデプロイ準備中）                     |
| API 機能  | ログの取得 (GET /logs)、ログの追加 (POST /logs) |

---

## ドキュメント一覧

このリポジトリには以下のドキュメントがあります。詳細は各ファイルを参照してください。

| ドキュメント                                               | 説明                     |
| ---------------------------------------------------- | ---------------------- |
| [Database Setup](docs/database_setup.md)             | SQLite データベースのセットアップ手順 |
| [Get Logs API](docs/get_logs_api.md)                 | GET /logs の仕様と動作説明     |
| [Post Logs API](docs/post_logs_api.md)               | POST /logs の仕様と動作説明    |
| [Terminal Commands](docs/terminal_commands.md)       | ターミナル操作のまとめ            |
| [Implementation Notes](docs/implementation_notes.md) | 実装の背景や技術的な補足           |

---

## 環境構築

### Anaconda を使用する場合

```sh
conda create --name flask_env python=3.9
conda activate flask_env
pip install -r requirements.txt
```

### venv を使用する場合

```sh
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## API の使い方

### ログを取得 (GET)

```sh
curl -X GET http://127.0.0.1:5001/logs
```

### ログを追加 (POST)

```sh
curl -X POST http://127.0.0.1:5001/logs \
     -H "Content-Type: application/json" \
     -d '{
           "log_level": "INFO",
           "message": "This is a test log."
         }'
```

---

## 今後の拡張予定

- エラーハンドリングの強化
- ログの検索 & フィルタリング機能
- AWS へのデプロイ（EC2, Lambda, S3 など）
- 認証機能の追加（JWTなど）
- フロントエンドとの統合（React or Vue）

---

## ライセンス

このプロジェクトは MIT ライセンスのもとで公開されています。

---

詳細な API 仕様やセットアップ手順は、各ドキュメントを参照してください。

