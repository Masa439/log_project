# GET /logs API ドキュメント

このドキュメントでは、`GET /logs` エンドポイントの詳細について説明します。

## **エンドポイント概要**

- **URL:** `/logs`
- **メソッド:** `GET`
- **機能:** データベースからログを取得し、オプションでフィルタリングを適用
- **レスポンス形式:** JSON

---

## **リクエストパラメータ（オプション）**

| パラメータ名  | 型       | 説明 |
|--------------|---------|------------------------------------------------|
| `level`      | `string` | 指定したログレベル (`INFO`, `WARNING`, `ERROR`, `DEBUG`) のみ取得 |
| `start`      | `string` | 指定した日付 (`YYYY-MM-DD`) 以降のログのみ取得 |
| `end`        | `string` | 指定した日付 (`YYYY-MM-DD`) 以前のログのみ取得 |

---

## **レスポンスフォーマット**

### **成功時 (200 OK)**
```json
[
    {
        "id": 123,
        "timestamp": "2025-02-23 14:30:12",
        "log_level": "INFO",
        "message": "System started successfully"
    },
    {
        "id": 124,
        "timestamp": "2025-02-23 14:45:32",
        "log_level": "ERROR",
        "message": "Database connection failed"
    }
]
```

### **エラー時 (500 Internal Server Error)**
```json
{
    "error": "Database error details"
}
```

---

## **使用例 (テスト方法)**

### **すべてのログを取得**
#### **cURL コマンド (Linux/macOS)**
```sh
curl -X GET "http://127.0.0.1:5001/logs"
```

#### **PowerShell コマンド (Windows)**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/logs" -Method GET
```

### **特定の条件でログを取得**
#### **`ERROR` レベルのログを取得**
```sh
curl -X GET "http://127.0.0.1:5001/logs?level=ERROR"
```

#### **特定の期間のログを取得**
```sh
curl -X GET "http://127.0.0.1:5001/logs?start=2025-02-20&end=2025-02-23"
```

---

## **処理の流れ (実装概要)**

1. **リクエストパラメータの取得**
    - クエリパラメータ (`level`, `start`, `end`) を取得
    - 指定されていない場合はすべてのログを取得

2. **データベースからデータを取得**
    - `sqlite3.connect()` でデータベースを開く
    - `SELECT * FROM logs WHERE 条件` を実行
    - `fetchall()` で取得したデータをリスト形式に変換

3. **成功レスポンスの返却**
    - `200 OK` でログデータを JSON として返す
    - エラー発生時は `500 Internal Server Error` を返す

---

## **トラブルシューティング**

### **1. `curl` のレスポンスが `500 Internal Server Error` になる**
**原因:** データベースの接続エラーや SQL クエリエラー
**対策:** `logs.db` のパスを確認し、DB が正しくセットアップされているか確認。

### **2. 期待したログが取得できない**
**原因:** フィルタリング条件が適切でない可能性。
**対策:** `level`, `start`, `end` の条件を変更し、意図したログが含まれるか確認。

---

このドキュメントは随時更新されます。

