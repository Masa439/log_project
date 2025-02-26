# UPDATE /logs API ドキュメント

このドキュメントでは、`PUT /logs` エンドポイントの詳細について説明します。

## **エンドポイント概要**

- **URL:** `/logs?id={log_id}`
- **メソッド:** `PUT`
- **機能:** 指定された `id` のログを更新する。
- **リクエスト形式:** JSON
- **レスポンス形式:** JSON

---

## **リクエストフォーマット**

```json
{
    "log_level": "DEBUG",
    "message": "Updated log message"
}
```

### **リクエストパラメータ**
| パラメータ名 | 型   | 必須 | 説明 |
|-------------|------|------|------|
| `log_level` | `string` | ✖ | ログのレベル (`INFO`, `WARNING`, `ERROR`, `DEBUG` など) |
| `message`   | `string` | ✖ | 更新するメッセージ内容 |

※ `log_level` または `message` のどちらか一方が必須。

---

## **レスポンスフォーマット**

### **成功時 (200 OK)**
```json
{
    "message": "Log with ID 123 updated successfully"
}
```

### **エラー時 (400 Bad Request)**
```json
{
    "error": "Missing 'id' parameter"
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
curl -X PUT "http://127.0.0.1:5001/logs?id=123" -H "Content-Type: application/json" -d '{
    "log_level": "DEBUG",
    "message": "Updated log message"
}'
```

### **PowerShell コマンド (Windows)**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?id=123" -Method PUT -Body (@{
    log_level="DEBUG";
    message="Updated log message"
} | ConvertTo-Json) -ContentType "application/json"
```

---

## **処理の流れ (実装概要)**

1. **リクエストデータの取得**
    - `request.get_json()` で JSON データを取得。
    - `id` パラメータが存在するかチェック。
    - `log_level` または `message` が含まれているかチェック。

2. **データベースの更新処理**
    - `sqlite3.connect()` でデータベースを開く。
    - `UPDATE logs SET log_level = ?, message = ? WHERE id = ?` を実行。
    - `commit()` して変更を保存。

3. **成功レスポンスの返却**
    - 正常に更新された場合、`200 OK` を返す。
    - エラー発生時は `500 Internal Server Error` を返し、エラーメッセージを含める。

---

## **トラブルシューティング**

### **1. `curl` のレスポンスが `400 Bad Request` になる**
**原因:** `id` パラメータが指定されていない、または `log_level` / `message` が不足している。
**対策:** 正しい JSON 形式でリクエストを送信する。

### **2. `500 Internal Server Error` になる**
**原因:** データベースエラーの可能性。
**対策:** `logs.db` のパスを確認し、DB が正しくセットアップされているか確認。

---

このドキュメントは随時更新されます。

