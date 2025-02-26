import sqlite3
import os

# データベースのパスを `data/` フォルダ内に設定
DB_FOLDER = "data"
DB_NAME = "logs.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

# `data/` フォルダが存在しない場合は作成
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

# データベースファイルを作成（なければ新規作成）
conn = sqlite3.connect(DB_PATH)
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

print(f"データベース '{DB_PATH}' を作成しました！")
