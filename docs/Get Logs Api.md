# `GET /logs` API の実装

このドキュメントでは、`GET /logs` エンドポイントの実装とその設計意図について詳しく説明します。

---

## **目的**

- ユーザーが保存されたログデータを取得できるようにする。
- フィルタリング（`log_level` や日付範囲）を可能にする。
- クライアントが効率的にログを取得できるよう、最新のログから取得する。

---

## **どのようにしてこのコードになったのか？**

### **1️⃣ API ルートを定義**
```python
@app.route("/logs", methods=["GET"])
```
- `@app.route()` で `GET /logs` のルートを作成。
- `methods=["GET"]` を指定し、POST ではアクセスできないように制限。

### **2️⃣ クエリパラメータの取得・バリデーション**
```python
log_level = request.args.get("level")
start_date = request.args.get("start")
end_date = request.args.get("end")
```
- `request.args.get("level")` で `log_level` のフィルタを取得。
- `start` と `end` を取得し、日付範囲での検索を可能にする。

### **3️⃣ SQL クエリの動的生成**
```python
query = "SELECT id, timestamp, log_level, message FROM logs"
filters = []
params = []

if log_level:
    filters.append("log_level = ?")
    params.append(log_level)
if start_date and end_date:
    filters.append("timestamp BETWEEN ? AND ?")
    params.extend([start_date, end_date])

if filters:
    query += " WHERE " + " AND ".join(filters)

query += " ORDER BY timestamp DESC LIMIT 100"
```
- ユーザーの入力に応じて `WHERE` 句を動的に作成。
- クエリを安全に実行するため `?` プレースホルダを使用。

### **4️⃣ データベースからデータを取得して JSON に変換**
```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute(query, params)
logs = cursor.fetchall()
conn.close()
```
- `sqlite3.connect(DB_PATH)` でデータベースに接続。
- クエリを実行し、取得したデータを `logs` に格納。

---

## **テスト方法**

### **1️⃣ サーバーを起動**
```sh
python3 app.py
```

### **2️⃣ `GET /logs` のテスト（curl を使用）**
```sh
curl -v http://127.0.0.1:5001/logs
```
**成功時のレスポンス（例）**
```json
[
    {
        "id": 1,
        "timestamp": "2025-02-23 12:30:00",
        "log_level": "INFO",
        "message": "System started."
    }
]
```

### **3️⃣ `GET /logs?level=ERROR` のテスト（エラーログのみ取得）**
```sh
curl -v "http://127.0.0.1:5001/logs?level=ERROR"
```

### **4️⃣ `GET /logs?start=YYYY-MM-DD&end=YYYY-MM-DD` のテスト（日付フィルタ）**
```sh
curl -v "http://127.0.0.1:5001/logs?start=2025-02-20&end=2025-02-23"
```

### **5️⃣ `GET /logs` の異常系テスト**
#### **❌ 存在しない `log_level` を指定 → 空の配列が返る**
```sh
curl -v "http://127.0.0.1:5001/logs?level=NON_EXISTENT"
```
**レスポンス（例）**
```json
[]
```

#### **❌ `start` または `end` が不正な形式 → 400 エラー**
```sh
curl -v "http://127.0.0.1:5001/logs?start=invalid_date&end=invalid_date"
```
**レスポンス**
```json
{
    "error": "Invalid date format"
}
```

---

## **トラブルシューティング**

### **1. `logs` テーブルが存在しないエラー**
- データベースのセットアップ (`database.py`) を実行したか確認。
- `sqlite3 logs.db` を開き、`SELECT * FROM logs;` でデータがあるか確認。

### **2. クライアントが `400 Bad Request` を受け取る**
- クエリパラメータ（`level` や `start`, `end`）が適切に指定されているか確認。
- `start` や `end` が `YYYY-MM-DD` の形式になっているか確認。

---



