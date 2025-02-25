import sqlite3

# データベースファイルを作成（なければ新規作成）
DB_NAME = "logs.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ログを保存するテーブルを作成
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        log_level TEXT,
        message TEXT
    )
""")

# 変更を保存してデータベースを閉じる
conn.commit()
conn.close()

print(f"データベース '{DB_NAME}' を作成しました！")
