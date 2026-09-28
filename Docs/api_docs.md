# MoMo SMS Transactions API — Documentation

Base URL: `http://localhost:8000`

All endpoints require **Basic Authentication**. Requests without valid
credentials receive a `401 Unauthorized` response.

---

## GET /transactions

Returns a list of all parsed SMS records.

**Fields on each transaction**
| Field | Description |
|---|---|
| id | Sequential record ID assigned during parsing |
| transaction_type | payment, transfer, bank_deposit, received, merchant_payment, bundle_purchase, withdrawal, reversal, failed, otp |
| amount | Amount in RWF |
| fee | Fee in RWF (null if the SMS does not state one) |
| new_balance | Account balance after the transaction (null if not stated) |
| counterparty | Name of the other party (null if none, e.g. bank deposits) |
| counterparty_phone | Phone number shown in the SMS, when present |
| financial_transaction_id | MoMo transaction ID (null for transfers and bank deposits, whose SMS has none) |
| timestamp | Transaction time (ISO format) |
| raw_body | Original SMS text |

**Request Example**
```bash
curl -u admin:momo123 http://localhost:8000/transactions
```

**Response Example** (200 OK)
```json
[
{
  "id": 1,
  "transaction_type": "received",
  "amount": 2000,
  "fee": null,
  "new_balance": 2000,
  "counterparty": "Jane Smith",
  "counterparty_phone": "*********013",
  "financial_transaction_id": "76662021700",
  "timestamp": "2024-05-10T16:30:51",
  "raw_body": "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. ..."
}
]
```

**Error Codes**
| Code | Meaning |
|---|---|
| 401 | Missing or invalid credentials |

---

## GET /transactions/{id}

Returns a single transaction by ID.

**Request Example**
```bash
curl -u admin:momo123 http://localhost:8000/transactions/1
```

**Response Example** (200 OK)
```json
{
  "id": 1,
  "transaction_type": "received",
  "amount": 2000,
  "fee": null,
  "new_balance": 2000,
  "counterparty": "Jane Smith",
  "counterparty_phone": "*********013",
  "financial_transaction_id": "76662021700",
  "timestamp": "2024-05-10T16:30:51",
  "raw_body": "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. ..."
}
```

**Error Codes**
| Code | Meaning |
|---|---|
| 401 | Missing or invalid credentials |
| 404 | Transaction with that ID does not exist |

---

## POST /transactions

Creates a new transaction. `id` is assigned automatically.

**Request Example**
```bash
curl -u admin:momo123 -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_type": "payment", "amount": 2000, "counterparty": "Bob"}'
```

**Response Example** (201 Created)
```json
{
  "id": 1692,
  "transaction_type": "payment",
  "amount": 2000,
  "counterparty": "Bob"
}
```

**Error Codes**
| Code | Meaning |
|---|---|
| 400 | Request body is not valid JSON |
| 401 | Missing or invalid credentials |

---

## PUT /transactions/{id}

Updates fields on an existing transaction. Only fields included in
the request body are changed.

**Request Example**
```bash
curl -u admin:momo123 -X PUT http://localhost:8000/transactions/1692 \
  -H "Content-Type: application/json" \
  -d '{"amount": 2500}'
```

**Response Example** (200 OK)
```json
{
  "id": 1692,
  "transaction_type": "payment",
  "amount": 2500,
  "counterparty": "Bob"
}
```

**Error Codes**
| Code | Meaning |
|---|---|
| 400 | Request body is not valid JSON |
| 401 | Missing or invalid credentials |
| 404 | Transaction with that ID does not exist |

---

## DELETE /transactions/{id}

Deletes a transaction by ID.

**Request Example**
```bash
curl -u admin:momo123 -X DELETE http://localhost:8000/transactions/1692
```

**Response Example** (200 OK)
```json
{
  "message": "Deleted",
  "transaction": {
    "id": 1692,
    "transaction_type": "payment",
    "amount": 2500,
    "counterparty": "Bob"
  }
}
```

**Error Codes**
| Code | Meaning |
|---|---|
| 401 | Missing or invalid credentials |
| 404 | Transaction with that ID does not exist |

---

## Notes on Security

This API uses **Basic Authentication**, which is simple to implement
but has real weaknesses:
- Credentials are only base64-encoded, not encrypted — trivially
  decodable if intercepted.
- No token expiry — credentials are the same on every request,
  forever, until manually changed.
- No support for scopes/permissions — it's all-or-nothing access.

Stronger alternatives for production use: **JWT** (short-lived,
signed tokens) or **OAuth2** (delegated authorization with scopes
and refresh tokens).