from flask import Flask, jsonify, request  # `request` を追加
import sqlite3
import os
from datetime import datetime  # `datetime` を追加

app = Flask(__name__)

# データベースのパスを定義
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

@app.route("/logs", methods=["GET"])
def get_logs():
    print("ログ取得リクエスト受信")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("データベース接続成功")

        cursor.execute("SELECT id, timestamp, log_level, message FROM logs ORDER BY timestamp DESC LIMIT 100")
        logs = cursor.fetchall()
        conn.close()
        
        print(f"取得したログ件数: {len(logs)}")  # ← 追加

        logs_list = [{"id": log[0], "timestamp": log[1], "log_level": log[2], "message": log[3]} for log in logs]

        return jsonify(logs_list)

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"error": str(e)}), 500


# 🚀 `POST /logs` のエンドポイントを追加 🚀
@app.route("/logs", methods=["POST"])
def add_log():
    print("ログ追加リクエスト受信")

    data = request.get_json()
    if not data or "log_level" not in data or "message" not in data:
        print("リクエストデータが不正")
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
        
        print(f"ログ追加成功: {log_level} - {message}")
        return jsonify({"message": "Log added successfully"}), 201

    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)  # ← 5001 に変更（5000 が AirPlay によって占有されていため）
