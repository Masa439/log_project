import sqlite3

def show_logs():
    """データベースからログを取得して表示"""
    conn = sqlite3.connect("logs.db")  # データベースに接続
    cursor = conn.cursor()
    
    # ログデータを取得
    cursor.execute("SELECT id, timestamp, log_level, message FROM logs ORDER BY timestamp DESC LIMIT 100")
    logs = cursor.fetchall()
    
    # データベースを閉じる
    conn.close()
    
    # 結果を表示
    for log in logs:
        log_id, timestamp, log_level, message = log
        print(f"[{timestamp}] {log_level}: {message}")

# 実行
if __name__ == "__main__":
    show_logs()
