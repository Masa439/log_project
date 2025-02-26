# GET /logs API

## **概要**
`GET /logs` API は、保存されたログデータを取得するためのエンドポイントです。クエリパラメータを使用することで、特定の条件でログをフィルタリングできます。

## **どのようにしてこのコードになったのか**
1. クエリパラメータ (`level`, `start`, `end`) を取得する
2. 取得した値に応じて SQL の `WHERE` 句を動的に変更する
3. SQLite データベースから該当するログを取得する
4. JSON 形式でレスポンスを返す

## **実装コード**
```python
import os
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# データベースのパスを定義
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

@app.route("/logs", methods=["GET"])
def get_logs():
    print("ログ取得リクエスト受信")

    # クエリパラメータを取得
    log_level = request.args.get("level")  # 例: "ERROR"
    start_date = request.args.get("start")  # 例: "2025-02-20"
    end_date = request.args.get("end")  # 例: "2025-02-23"

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("データベース接続成功")

        # SQL クエリの動的生成
        query = "SELECT id, timestamp, log_level, message FROM logs WHERE 1=1"
        params = []

        # ログレベルでフィルタリング
        if log_level:
            query += " AND log_level = ?"
            params.append(log_level)

        # 期間指定でフィルタリング
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " ORDER BY timestamp DESC LIMIT 100"

        cursor.execute(query, params)
        logs = cursor.fetchall()
        conn.close()

        print(f"取得したログ件数: {len(logs)}")

        logs_list = [{"id": log[0], "timestamp": log[1], "log_level": log[2], "message": log[3]} for log in logs]

        return jsonify(logs_list)

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

## **テスト方法**
### **1. 全ログを取得**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs" -Method GET
```

### **2. `ERROR` レベルのログのみ取得**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?level=ERROR" -Method GET
```

### **3. 期間指定で取得**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?start=2025-02-20&end=2025-02-23" -Method GET
```

### **4. `ERROR` レベルのログで期間指定**
```sh
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?level=ERROR&start=2025-02-20&end=2025-02-23" -Method GET
```

## **今後の改善点**
- 取得件数を指定できるようにする（`limit=50` など）
- ログのソート順を指定できるようにする（`sort=asc` / `sort=desc`）

