# POST /logs API ドキュメント

このドキュメントでは、`POST /logs` エンドポイントの詳細について説明します。

## **エンドポイント概要**

- **URL:** `/logs`
- **メソッド:** `POST`
- **機能:** 新しいログを作成し、データベースに保存する。
- **リクエスト形式:** JSON
- **レスポンス形式:** JSON

---

## **リクエストフォーマット**

```json
{
    "log_level": "INFO",
    "message": "This is a test log."
}
```

### **リクエストパラメータ**
| パラメータ名 | 型   | 必須 | 説明 |
|-------------|------|------|------|
| `log_level` | `string` | ✔ | ログのレベル (`INFO`, `WARNING`, `ERROR`, `DEBUG` など) |
| `message`   | `string` | ✔ | ログの内容 |

---

## **レスポンスフォーマット**

### **成功時 (201 Created)**
```json
{
    "message": "Log added successfully"
}
```

### **エラー時 (400 Bad Request)**
```json
{
    "error": "Invalid request"
}
```

### **エラー時 (500 Internal Server Error)**
```json
{
    "error": "Database error details"
}
```

---

## **使用例 (テスト方法)**

### **cURL コマンド (Linux/macOS)**
```sh
curl -X POST http://127.0.0.1:5001/logs -H "Content-Type: application/json" -d '{
    "log_level": "INFO",
    "message": "This is a test log."
}'
```

### **PowerShell コマンド (Windows)**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs" -Method POST -Body (@{
    log_level="INFO";
    message="This is a test log."
} | ConvertTo-Json) -ContentType "application/json"
```

---

## **処理の流れ (実装概要)**

1. **リクエストデータの取得**
    - `request.get_json()` で JSON データを取得。
    - `log_level` と `message` が含まれているかチェック。

2. **データベースにデータを挿入**
    - `sqlite3.connect()` でデータベースを開く。
    - `INSERT INTO logs (log_level, message) VALUES (?, ?)` を実行。
    - `commit()` して変更を保存。

3. **成功レスポンスの返却**
    - 正常に追加された場合、`201 Created` を返す。
    - エラー発生時は `500 Internal Server Error` を返し、エラーメッセージを含める。

---

## **トラブルシューティング**

### **1. `curl` のレスポンスが `400 Bad Request` になる**
**原因:** `log_level` や `message` のパラメータが不足している。
**対策:** 正しい JSON 形式でリクエストを送信する。

### **2. `500 Internal Server Error` になる**
**原因:** データベースエラーの可能性。
**対策:** `logs.db` のパスを確認し、DB が正しくセットアップされているか確認。

---

このドキュメントは随時更新されます。

