# SQLite データベースのセットアップ

このドキュメントでは、Flask ログ管理 API のデータベースセットアップについて詳しく記述します。

---

## **目的**

- ログを保存するための `logs.db` を作成し、テーブル `logs` を定義。
- テーブルのカラム: `id, timestamp, log_level, message`。
- SQLite はシンプルでセットアップが簡単なため選択。
- `AUTOINCREMENT` を使用して `id` を自動増分させる設計。

---

## **どのようにしてこのコードになったのか？**

### **1️⃣ データベースファイルのパスを設定**

```python
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")
```

- `os.path.join()` を使うことで、異なる OS でも適切にパスが解釈される。
- `__file__` を使用し、現在のスクリプトがあるフォルダ内にデータベースファイルを作成。

### **2️⃣ SQLite データベースに接続**

```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
```

- `sqlite3.connect(DB_PATH)` でデータベース接続。
- `cursor = conn.cursor()` でデータ操作用のカーソルを作成。

### **3️⃣ テーブル作成**

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        log_level TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")
```

- `CREATE TABLE IF NOT EXISTS` を使用し、スクリプトの複数回実行を安全にする。
- `TEXT NOT NULL` にすることで、データの空値を防ぐ。
- `AUTOINCREMENT` により `id` を自動で増加させる。

### **4️⃣ 変更を確定し、接続を閉じる**

```python
conn.commit()
conn.close()
```

- `commit()` でデータベースの変更を保存。
- `close()` で接続を閉じ、リソースを解放。

---

## **実装コード (`database.py`)**

```python
import sqlite3
import os

# データベースのパスを設定
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

# SQLiteデータベースに接続
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# テーブルが存在しない場合のみ作成
cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        log_level TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

# 変更を保存して接続を閉じる
conn.commit()
conn.close()
```

---

## **テスト方法**

### **1️⃣ SQLite データベースの作成**
```sh
python database.py
```
- `database.py` を実行すると、`data/logs.db` に SQLite データベースが作成される。

### **2️⃣ `logs` テーブルの作成確認**
```sh
sqlite3 data/logs.db "SELECT name FROM sqlite_master WHERE type='table';"
```
**レスポンス（例）**
```
logs
```

### **3️⃣ `logs` テーブルのスキーマを表示**
```sh
sqlite3 data/logs.db ".schema logs"
```

### **4️⃣ `logs` テーブルのデータを取得**
```sh
sqlite3 data/logs.db "SELECT * FROM logs;"
```

### **5️⃣ データの追加を手動でテスト**
```sh
sqlite3 data/logs.db "INSERT INTO logs (timestamp, log_level, message) VALUES ('2025-02-23 14:30:00', 'INFO', 'Manual log entry');"
```
**追加後に確認**
```sh
sqlite3 data/logs.db "SELECT * FROM logs;"
```

### **6️⃣ `logs` テーブルをリセット（データ削除）**
```sh
sqlite3 data/logs.db "DELETE FROM logs;"
```

---

## **トラブルシューティング**

### **1. `logs.db` が作成されない**
- `database.py` を実行しても `data/logs.db` が作成されていない場合：
  - `data/` フォルダが存在するか確認 (`mkdir data` で作成)
  - `sqlite3.connect(DB_PATH)` の `DB_PATH` を `print(DB_PATH)` で確認

### **2. `logs` テーブルがないエラー**
```sh
sqlite3 data/logs.db "SELECT name FROM sqlite_master WHERE type='table';"
```
- `logs` テーブルが表示されない場合は、`database.py` を再実行。

### **3. `logs` テーブルを初期化（すべてのデータを削除）**
```sh
sqlite3 data/logs.db "DELETE FROM logs;"
```

---

