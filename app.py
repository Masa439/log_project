import os
import csv
import sqlite3
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# データベースのパスを定義
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

# ✅ ログの取得 (フィルタリング対応)
@app.route("/logs", methods=["GET"])
def get_logs():
    print("ログ取得リクエスト受信")

    log_level = request.args.get("level")
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("データベース接続成功")

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

# ✅ ログの登録
@app.route("/logs", methods=["POST"])
def add_log():
    data = request.get_json()
    if not data or "log_level" not in data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    log_level = data["log_level"]
    message = data["message"]

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (log_level, message) VALUES (?, ?)", (log_level, message))
        conn.commit()
        conn.close()

        return jsonify({"message": "Log added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ログの削除 (ID指定 or 全削除)
@app.route("/logs", methods=["DELETE"])
def delete_log():
    log_id = request.args.get("id")
    delete_all = request.args.get("all")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if delete_all == "true":
            cursor.execute("DELETE FROM logs")
            message = "All logs deleted successfully"
        elif log_id:
            cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
            message = f"Log with ID {log_id} deleted successfully"
        else:
            return jsonify({"error": "Invalid request. Provide 'id' or 'all=true'"}), 400

        conn.commit()
        conn.close()

        return jsonify({"message": message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ログの更新 (ID指定で log_level または message を変更)
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

# ✅ ログの統計情報取得
@app.route("/logs/stats", methods=["GET"])
def get_log_stats():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM logs")
        total_logs = cursor.fetchone()[0]

        cursor.execute("SELECT log_level, COUNT(*) FROM logs GROUP BY log_level")
        log_counts = cursor.fetchall()
        conn.close()

        log_level_counts = {level: count for level, count in log_counts}

        return jsonify({
            "total_logs": total_logs,
            "log_levels": log_level_counts
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ログの検索 (message 内の部分一致検索)
@app.route("/logs/search", methods=["GET"])
def search_logs():
    query_param = request.args.get("query")
    if not query_param:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, log_level, message FROM logs WHERE message LIKE ?", (f"%{query_param}%",))
        logs = cursor.fetchall()
        conn.close()

        logs_list = [{"id": log[0], "timestamp": log[1], "log_level": log[2], "message": log[3]} for log in logs]
        return jsonify(logs_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ ログのエクスポート (JSON or CSV)
@app.route("/logs/export", methods=["GET"])
def export_logs():
    export_format = request.args.get("format", "json").lower()

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, log_level, message FROM logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        conn.close()

        if export_format == "csv":
            def generate_csv():
                yield "id,timestamp,log_level,message\n"
                for log in logs:
                    yield f"{log[0]},{log[1]},{log[2]},{log[3]}\n"

            return Response(generate_csv(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=logs.csv"})

        else:
            logs_list = [{"id": log[0], "timestamp": log[1], "log_level": log[2], "message": log[3]} for log in logs]
            return jsonify(logs_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
