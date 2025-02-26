# Implementation Notes

このドキュメントでは、Flask ログ管理 API の実装に関する詳細な情報を提供します。

## **1. プロジェクト概要**
このプロジェクトは、Flask と SQLite を使用してログを管理するシステムです。以下の機能を実装しています。
- ログの追加 (`POST /logs`)
- ログの取得 (`GET /logs`)
- ログの更新 (`PUT /logs`)
- ログの削除 (`DELETE /logs`)
- ログの統計取得 (`GET /logs/stats`)

---

## **2. データベース設計**

### **テーブル: logs**
| カラム名   | 型          | 説明 |
|------------|------------|------------------------------------------------|
| `id`       | `INTEGER`  | プライマリキー（自動インクリメント） |
| `timestamp`| `TEXT`     | ログの作成日時（デフォルトで現在時刻） |
| `log_level`| `TEXT`     | ログのレベル (`INFO`, `WARNING`, `ERROR`, `DEBUG`) |
| `message`  | `TEXT`     | ログの内容 |

データベースのセットアップは `database.py` を実行することで `data/logs.db` に `logs` テーブルが作成されます。

---

## **3. 各エンドポイントの実装**

### **3.1 ログの追加 (`POST /logs`)
- `request.get_json()` でリクエストデータを取得
- `log_level` および `message` を検証
- `INSERT INTO logs (log_level, message) VALUES (?, ?)` を実行
- 成功時は `201 Created` を返す

### **3.2 ログの取得 (`GET /logs`)
- クエリパラメータ (`level`, `start`, `end`) を取得
- `SELECT * FROM logs WHERE 条件` でログを取得
- 取得結果を JSON で返す

### **3.3 ログの更新 (`PUT /logs`)
- `id` パラメータを取得
- `log_level` または `message` を取得し `UPDATE logs SET ... WHERE id = ?` を実行
- 成功時は `200 OK` を返す

### **3.4 ログの削除 (`DELETE /logs`)
- `id` または `all=true` のリクエストを受け取る
- `DELETE FROM logs WHERE id = ?` または `DELETE FROM logs` を実行
- 成功時は `200 OK` を返す

### **3.5 ログの統計取得 (`GET /logs/stats`)
- `SELECT COUNT(*) FROM logs` で総件数を取得
- `SELECT log_level, COUNT(*) FROM logs GROUP BY log_level` で各レベルの件数を取得
- JSON でレスポンスを返す

---

## **4. エラーハンドリング**
- **`400 Bad Request`**: リクエストデータの不足 (`log_level`, `message` が無いなど)
- **`500 Internal Server Error`**: データベース接続エラーや SQL 実行エラー

---

## **5. 開発環境のセットアップ**
- `conda create --name flask_env python=3.9`
- `conda activate flask_env`
- `pip install -r requirements.txt`

サーバー起動:
```sh
python3 app.py
```

---

このドキュメントは随時更新されます。

