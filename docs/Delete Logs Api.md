# DELETE /logs API ドキュメント

このドキュメントでは、`DELETE /logs` エンドポイントの詳細について説明します。

## **エンドポイント概要**

- **URL:** `/logs`
- **メソッド:** `DELETE`
- **機能:** 指定された `id` のログを削除、またはすべてのログを削除。
- **リクエスト形式:** クエリパラメータ
- **レスポンス形式:** JSON

---

## **リクエストパラメータ**

| パラメータ名  | 型       | 必須 | 説明 |
|--------------|---------|------|------------------------------------------------|
| `id`         | `string` | ✖ | 指定したログIDのログを削除 |
| `all`        | `string` | ✖ | `all=true` を指定すると、全ログを削除 |

※ `id` または `all=true` のどちらかを指定する必要があります。

---

## **レスポンスフォーマット**

### **成功時 (200 OK)**
```json
{
    "message": "Log with ID 123 deleted successfully"
}
```
または
```json
{
    "message": "All logs deleted successfully"
}
```

### **エラー時 (400 Bad Request)**
```json
{
    "error": "Invalid request. Provide 'id' or 'all=true'"
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

### **特定のログを削除**
#### **cURL コマンド (Linux/macOS)**
```sh
curl -X DELETE "http://127.0.0.1:5001/logs?id=123"
```

#### **PowerShell コマンド (Windows)**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?id=123" -Method DELETE
```

### **すべてのログを削除**
#### **cURL コマンド (Linux/macOS)**
```sh
curl -X DELETE "http://127.0.0.1:5001/logs?all=true"
```

#### **PowerShell コマンド (Windows)**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs?all=true" -Method DELETE
```

---

## **処理の流れ (実装概要)**

1. **クエリパラメータの取得**
    - `id` または `all` を取得し、リクエストの正当性を確認。

2. **データベースの削除処理**
    - `DELETE FROM logs WHERE id = ?` または `DELETE FROM logs` を実行。
    - `commit()` して変更を保存。

3. **成功レスポンスの返却**
    - 正常に削除された場合、`200 OK` を返す。
    - エラー発生時は `500 Internal Server Error` を返す。

---

## **トラブルシューティング**

### **1. `curl` のレスポンスが `400 Bad Request` になる**
**原因:** `id` または `all=true` のどちらも指定されていない。
**対策:** 適切なパラメータを指定してリクエストを送信。

### **2. `500 Internal Server Error` になる**
**原因:** データベースの接続エラーや SQL 実行エラーの可能性。
**対策:** `logs.db` のパスを確認し、DB が正しくセットアップされているか確認。

---

このドキュメントは随時更新されます。

