# 実装の記録 (Implementation Notes)

このドキュメントでは、Flask ログ管理 API の全体像と設計の概要をまとめています。
詳細な実装は各機能ごとのドキュメントに記載しています。

---

## **全体の概要**
### **目的**
- ログデータを管理する API を Flask + SQLite で構築。
- ログの記録 (`POST /logs`)、取得 (`GET /logs`)、将来的には削除 (`DELETE /logs/:id`)、更新 (`PUT /logs/:id`) を提供。
- SQLite を利用することでセットアップを簡単にし、開発環境でも手軽に動作するように設計。

---

## **API の構成**

| API エンドポイント | 説明 | 詳細ドキュメント |
|--------------------|------------------------------------|----------------|
| `GET /logs` | すべてのログを取得（フィルタ機能あり） | [GET /logs の詳細](get_logs_api.md) |
| `POST /logs` | 新しいログを追加 | [POST /logs の詳細](post_logs_api.md) |
| `DELETE /logs/:id` | 指定した ID のログを削除（予定） | **未実装** |
| `PUT /logs/:id` | 指定した ID のログを更新（予定） | **未実装** |

---

## **主要コンポーネントとその役割**

| ファイル | 役割 | 詳細ドキュメント |
|---------|-------------------------------|----------------|
| `database.py` | SQLite データベースのセットアップ | [データベースセットアップ](database_setup.md) |
| `app.py` | Flask アプリケーションのエントリーポイント | **本ドキュメント** |
| `get_logs_api.md` | `GET /logs` の設計・実装の詳細 | [GET /logs の詳細](get_logs_api.md) |
| `post_logs_api.md` | `POST /logs` の設計・実装の詳細 | [POST /logs の詳細](post_logs_api.md) |

---

## **開発の流れ**
### **1️⃣ データベースの準備**
データを保存する SQLite の `logs.db` を作成し、必要なテーブル `logs` を作成する。
```python
import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        log_level TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")
conn.commit()
conn.close()
```
➡ **詳細は [データベースセットアップ](database_setup.md) を参照**

### **2️⃣ ログを取得する API (`GET /logs`) の実装**
- すべてのログを取得できる。
- `log_level`, `start`, `end` でフィルタ可能。
- SQL インジェクション対策のため `?` プレースホルダーを使用。
```python
@app.route("/logs", methods=["GET"])
def get_logs():
    log_level = request.args.get("level")
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    query = "SELECT id, timestamp, log_level, message FROM logs WHERE 1=1"
    params = []
    if log_level:
        query += " AND log_level = ?"
        params.append(log_level)
    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)
    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()
    return jsonify([{"id": log[0], "timestamp": log[1], "log_level": log[2], "message": log[3]} for log in logs])
```
➡ **詳細は [GET /logs の詳細](get_logs_api.md) を参照**

### **3️⃣ ログを追加する API (`POST /logs`) の実装**
- ユーザーが新しいログ (`log_level`, `message`) を送信。
- `timestamp` はサーバー側で生成。
- データを SQLite に保存。
```python
@app.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    if not data or "log_level" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400
    log_level = data["log_level"]
    message = data["message"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (timestamp, log_level, message) VALUES (?, ?, ?)",
            (timestamp, log_level, message),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Log added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```
➡ **詳細は [POST /logs の詳細](post_logs_api.md) を参照**

---

## **今後の開発予定**
### **✅ 実装済み**
- `GET /logs` : ログの取得
- `POST /logs` : ログの追加

### **🛠 実装予定**
- `DELETE /logs/:id` : 指定したログを削除
- `PUT /logs/:id` : 指定したログを更新
- **フロントエンドの実装** : Web UI を作成し、ログを閲覧・管理できるようにする

---

このドキュメントは随時更新していきます。

