# Flask ログ管理 API

このプロジェクトは、Flask + SQLite を使用してログデータを管理する API です。
ログの取得、フィルタリング、作成、更新、削除、統計情報の取得が可能です。

---

## 環境構築

### 1. Anaconda (`conda`) を使用する場合

#### 環境の作成

```sh
conda create --name flask_env python=3.9
```

#### 環境をアクティブ化

```sh
conda activate flask_env
```

#### 必要なライブラリをインストール

```sh
pip install -r requirements.txt
```

---

### 2. `venv` を使用する場合

#### 仮想環境を作成

```sh
python3 -m venv venv
```

#### 仮想環境をアクティブ化

```sh
# Mac/Linux の場合
source venv/bin/activate

# Windows PowerShell の場合
venv\Scripts\activate
```

#### 必要なライブラリをインストール

```sh
pip install -r requirements.txt
```

---

## データベースのセットアップ

```sh
python database.py
```

成功すると `data/logs.db` が作成され、`logs` テーブルが準備されます。

---

## API の使い方

### 1. すべてのログを取得（フィルタリング可能）

```sh
curl -X GET "http://127.0.0.1:5001/logs"
```

フィルタリングオプション:

```sh
curl -X GET "http://127.0.0.1:5001/logs?level=ERROR&start=2025-02-20&end=2025-02-23"
```

### 2. 新しいログを追加

```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "INFO",
    "message": "This is a test log."
}'
```

### 3. ログを更新

```sh
curl -X PUT "http://127.0.0.1:5001/logs?id=123" -H "Content-Type: application/json" -d '{
    "log_level": "DEBUG",
    "message": "Updated log message"
}'
```

### 4. ログを削除

- 特定のログを削除

```sh
curl -X DELETE "http://127.0.0.1:5001/logs?id=123"
```

- すべてのログを削除

```sh
curl -X DELETE "http://127.0.0.1:5001/logs?all=true"
```

### 5. ログ統計情報を取得

```sh
curl -X GET "http://127.0.0.1:5001/logs/stats"
```

レスポンス例:

```json
{
    "total_logs": 100,
    "log_levels": {
        "INFO": 40,
        "WARNING": 30,
        "ERROR": 20,
        "DEBUG": 10
    }
}
```

---

## サーバーの起動方法

```sh
python3 app.py
```

成功すると、以下のように表示されます。

```
* Running on http://127.0.0.1:5001/
```

Flask を起動したままにすること (`CTRL + C` で止めないこと)

---

## サーバーの終了

```sh
CTRL + C
```

---

## トラブルシューティング

### 1. `curl` が `Connection refused` になる

```sh
netstat -an | grep 5001  # Mac/Linux
netstat -an | findstr 5001  # Windows
```

### 2. `5001` のポートが AirPlay によって占有されている

```sh
lsof -i :5001  # Mac/Linux
netstat -ano | findstr :5001  # Windows
```

ポートを占有しているプロセスを特定し、終了する。

```sh
kill -9 <プロセスID>  # Mac/Linux
taskkill /PID <プロセスID> /F  # Windows
```

