# Database Setup

このドキュメントでは、Flask ログ管理 API で使用する SQLite データベースのセットアップについて説明します。

---

## **1. データベース概要**

この API は SQLite を使用してログデータを管理します。データベース `logs.db` には、以下のテーブル `logs` が格納されます。

### **テーブル: logs**
| カラム名   | 型          | 説明 |
|------------|------------|------------------------------------------------|
| `id`       | `INTEGER`  | プライマリキー（自動インクリメント） |
| `timestamp`| `TEXT`     | ログの作成日時（デフォルトで現在時刻） |
| `log_level`| `TEXT`     | ログのレベル (`INFO`, `WARNING`, `ERROR`, `DEBUG`) |
| `message`  | `TEXT`     | ログの内容 |

---

## **2. データベースの作成手順**

### **データベースセットアップスクリプト (`database.py`)**
以下のスクリプトを実行することで、データベースが作成されます。

```python
import sqlite3
import os

# データベースのパスを設定
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "logs.db")

# データベース接続
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# logs テーブルの作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        log_level TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# 変更を保存して接続を閉じる
conn.commit()
conn.close()
print(f"データベース '{DB_PATH}' を作成しました！")
```

### **実行方法**
```sh
python database.py
```

実行後、`data/logs.db` が作成され、`logs` テーブルがセットアップされます。

---

## **3. データベースの操作方法**

### **データベースの内容を確認**
#### **全ログの取得**
```sh
sqlite3 data/logs.db "SELECT * FROM logs;"
```

### **特定のログレベルのログを取得**
```sh
sqlite3 data/logs.db "SELECT * FROM logs WHERE log_level = 'ERROR';"
```

### **ログの削除**
```sh
sqlite3 data/logs.db "DELETE FROM logs WHERE id = 1;"
```

### **データベースのリセット（全削除）**
```sh
sqlite3 data/logs.db "DELETE FROM logs;"
```

---

## **4. トラブルシューティング**

### **1. `logs.db` が作成されない**
**原因:** `data/` フォルダが存在しない可能性。
**対策:** `mkdir data` コマンドで `data/` フォルダを作成し、`database.py` を再実行。

### **2. `sqlite3` コマンドが使えない**
**原因:** SQLite がインストールされていない可能性。
**対策:** `sqlite3` のインストールを確認し、必要に応じてインストール。

### **3. `OperationalError: no such table: logs` が発生する**
**原因:** データベースが正しく作成されていない可能性。
**対策:** `database.py` を再実行して `logs` テーブルを作成。

---

このドキュメントは随時更新されます。

