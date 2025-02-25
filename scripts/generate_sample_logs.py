import sqlite3
import random
import datetime

# データベースに接続（存在しなければ作成）
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# ログレベルのリスト
log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]

# ログメッセージのリスト
messages = [
    "User logged in",
    "Database connection failed",
    "High memory usage detected",
    "File uploaded successfully",
    "API request failed with status 500",
    "Authentication failed",
    "CPU temperature too high",
    "User logged out",
    "Disk space running low",
    "Configuration updated"
]

# 現在の時刻を基準にランダムな時間を作る
now = datetime.datetime.now()

# 1000件のランダムなログデータを作成
log_entries = []
for _ in range(1000):  # 必要なデータ数を指定（ここでは1000件）
    timestamp = now - datetime.timedelta(minutes=random.randint(0, 43200))  # 過去30日間のランダムな時間
    log_level = random.choice(log_levels)
    message = random.choice(messages)
    log_entries.append((timestamp.strftime("%Y-%m-%d %H:%M:%S"), log_level, message))

# データを一括挿入
cursor.executemany("INSERT INTO logs (timestamp, log_level, message) VALUES (?, ?, ?)", log_entries)

# 変更を保存して接続を閉じる
conn.commit()
conn.close()

print("✅ 1000件のサンプルログデータを作成しました！")
