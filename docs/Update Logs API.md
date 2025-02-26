# PUT /logs API

## **概要**
`PUT /logs` API は、特定のログの `log_level` や `message` を更新するためのエンドポイントです。

## **どのようにしてこのコードになったのか**
1. クエリパラメータ `id` を取得し、更新対象のログを特定する。
2. `log_level` や `message` のどちらかがリクエストボディに含まれている場合、それを更新対象とする。
3. SQLite を使ってデータベースの該当ログを更新。
4. 更新が成功したらメッセージを返す。

## **実装コード**
```python
@app.route("/logs", methods=["PUT"])
def update_log():
    data = request.get_json()
    log_id = request.args.get("id")

    if not log_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    update_fields = []
    params = []

    if "log_level" in data:
        update_fields.append("log_level = ?")
        params.append(data["log_level"])

    if "message" in data:
        update_fields.append("message = ?")
        params.append(data["message"])

    if not update_fields:
        return jsonify({"error": "No update fields provided"}), 400

    params.append(log_id)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = f"UPDATE logs SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()

        return jsonify({"message": f"Log with ID {log_id} updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

## **テスト方法**
### **1. ログの `log_level` を変更**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?id=123" -Method PUT -Body (@{log_level="ERROR"} | ConvertTo-Json) -ContentType "application/json"
```
📌 **ID `123` のログの `log_level` を `ERROR` に変更**

### **2. `message` のみ変更**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?id=123" -Method PUT -Body (@{message="Updated message"} | ConvertTo-Json) -ContentType "application/json"
```
📌 **ID `123` の `message` を `Updated message` に変更**

### **3. 両方 (`log_level` & `message`) を変更**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?id=123" -Method PUT -Body (@{log_level="DEBUG"; message="New debug message"} | ConvertTo-Json) -ContentType "application/json"
```
📌 **ID `123` の `log_level` を `DEBUG`、`message` を `New debug message` に変更**

## **今後の改善点**
- `updated_at` のタイムスタンプを追加し、更新時刻を記録する。
- 変更前のデータと変更後のデータを返すようにする。
- ログが存在しない場合、エラーを返す処理を追加する。

