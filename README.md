# Flask ログ管理 API

このプロジェクトは、Flask + SQLite を使用してログデータを管理する API です。
ログの取得やフィルタリングを行うことができます。

---

## 環境構築

### 1. Anaconda (`conda`) を使用する場合（推奨）
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

### 2. `venv` を使用する場合（オプション）
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

## API の使い方

### 1. すべてのログを取得
```sh
curl -v http://127.0.0.1:5001/logs
```

### 2. 特定のログレベル（ERROR など）を取得
```sh
curl -v "http://127.0.0.1:5001/logs?level=ERROR"
```

### 3. 特定の日付範囲のログを取得
```sh
curl -v "http://127.0.0.1:5001/logs?start=2025-02-20&end=2025-02-23"
```

---

## サーバーの終了

```sh
CTRL + C
```

---

## トラブルシューティング

### 1. `curl` が `Connection refused` になる
```sh
netstat -an | grep 5001
```

### 2. `5001` のポートが AirPlay によって占有されている
```sh
lsof -i :5001
kill -9 <プロセスID>
```

