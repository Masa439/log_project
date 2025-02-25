# `POST /logs` API の実装

このドキュメントでは、`POST /logs` エンドポイントの実装とその設計意図について詳しく説明します。

---

## **目的**

- ユーザーが新しいログ (`log_level` と `message`) を送信し、それをデータベースに保存する。
- `timestamp` はサーバー側で自動生成する。
- クライアントが不正なデータを送らないようバリデーションを行う。

---

## **どのようにしてこのコードになったのか？**

### **1️⃣ API ルートを定義**
```python
@app.route("/logs", methods=["POST"])
```
- `@app.route()` で `POST /logs` のルートを作成。
- `methods=["POST"]` を指定し、GET ではアクセスできないように制限。

### **2️⃣ クライアントのデータを取得・バリデーション**
```python
data = request.get_json()
if not data or "log_level" not in data or "message" not in data:
    return jsonify({"error": "Invalid request"}), 400
```
- `request.get_json()` で JSON を取得。
- `log_level` と `message` が含まれているかチェック。
- もし `log_level` や `message` が無ければ `400 Bad Request` を返す。

### **3️⃣ `timestamp` をサーバー側で作成**
```python
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```
- `datetime.now()` で現在の時刻を取得し、適切なフォーマットに変換。
- クライアント側から送信させないことで、改ざんを防ぐ。

### **4️⃣ データベースにログを追加**
```python
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
- `sqlite3.connect(DB_PATH)` でデータベースに接続。
- `INSERT INTO logs ...` を実行し、新しいログを挿入。
- `try-except` を使用し、エラーが発生した場合 `500 Internal Server Error` を返す。

---

## **テスト方法**

### **1️⃣ サーバーを起動**
```sh
python3 app.py
```

### **2️⃣ `POST /logs` のテスト（curl を使用）**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "INFO",
    "message": "This is a test log."
}'
```
**成功時のレスポンス**
```json
{
    "message": "Log added successfully"
}
```

### **3️⃣ データベースにデータが入ったか確認**
```sh
sqlite3 data/logs.db "SELECT * FROM logs;"
```

### **4️⃣ エラーパターンテスト**
#### **❌ `log_level` なし → `400 Bad Request`**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "message": "Missing log level."
}'
```
**レスポンス**
```json
{
    "error": "Invalid request"
}
```

#### **❌ `message` なし → `400 Bad Request`**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "ERROR"
}'
```
**レスポンス**
```json
{
    "error": "Invalid request"
}
```

#### **❌ JSON ではなく文字列を送信 → `400 Bad Request`**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d 'Invalid Data'
```
**レスポンス**
```json
{
    "error": "Invalid request"
}
```

#### **✅ 正常データと異常データの連続送信テスト**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "DEBUG",
    "message": "This is a debug log."
}'

curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "ERROR"
}'
```
**最初のリクエストは成功し、2つ目は `400 Bad Request` になることを確認する。**

---

## **トラブルシューティング**

### **1. `logs` テーブルが存在しないエラー**
- データベースのセットアップ (`database.py`) を実行したか確認。
- `sqlite3 logs.db` を開き、`SELECT * FROM logs;` でデータがあるか確認。

### **2. クライアントが `400 Bad Request` を受け取る**
- 送信している JSON が正しいか確認。
- `log_level` や `message` を必ず含めること。
- 例:
```json
{
    "log_level": "ERROR",
    "message": "An error occurred."
}
```

---



