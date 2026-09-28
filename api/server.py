import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from auth import check_auth, build_401_body

# ---------------------------------------------------------------
# In-memory data store, loaded from Person A's parsed JSON output.
# Dict keyed by id -> O(1) average lookup, matching the DSA task.
# ---------------------------------------------------------------
TRANSACTIONS = {}


def load_data(json_path="../dsa/transactions.json"):
    global TRANSACTIONS
    with open(json_path, "r", encoding="utf-8") as f:
        records = json.load(f)
    TRANSACTIONS = {record["id"]: record for record in records}


class TransactionHandler(BaseHTTPRequestHandler):

    def _send_json(self, status_code: int, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def _authenticate(self) -> bool:
        auth_header = self.headers.get("Authorization")
        if not check_auth(auth_header):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(build_401_body()).encode("utf-8"))
            return False
        return True

    def _get_id_from_path(self):
        """Extracts the {id} from /transactions/{id}, or None if absent/invalid."""
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                return int(parts[1])
            except ValueError:
                return None
        return None

    # --------------------- GET ---------------------
    def do_GET(self):
        if not self._authenticate():
            return

        path = urlparse(self.path).path
        txn_id = self._get_id_from_path()

        if path == "/transactions":
            self._send_json(200, list(TRANSACTIONS.values()))
        elif txn_id is not None:
            transaction = TRANSACTIONS.get(txn_id)
            if transaction:
                self._send_json(200, transaction)
            else:
                self._send_json(404, {"error": "Transaction not found"})
        else:
            self._send_json(404, {"error": "Not found"})

    # --------------------- POST ---------------------
    def do_POST(self):
        if not self._authenticate():
            return

        if urlparse(self.path).path != "/transactions":
            self._send_json(404, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            new_transaction = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        new_id = max(TRANSACTIONS.keys(), default=0) + 1
        new_transaction["id"] = new_id
        TRANSACTIONS[new_id] = new_transaction

        self._send_json(201, new_transaction)

    # --------------------- PUT ---------------------
    def do_PUT(self):
        if not self._authenticate():
            return

        txn_id = self._get_id_from_path()
        if txn_id is None or txn_id not in TRANSACTIONS:
            self._send_json(404, {"error": "Transaction not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            updates = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        TRANSACTIONS[txn_id].update(updates)
        self._send_json(200, TRANSACTIONS[txn_id])

    # --------------------- DELETE ---------------------
    def do_DELETE(self):
        if not self._authenticate():
            return

        txn_id = self._get_id_from_path()
        if txn_id is None or txn_id not in TRANSACTIONS:
            self._send_json(404, {"error": "Transaction not found"})
            return

        deleted = TRANSACTIONS.pop(txn_id)
        self._send_json(200, {"message": "Deleted", "transaction": deleted})


def run(port: int = 8000):
    load_data()
    server = HTTPServer(("localhost", port), TransactionHandler)
    print(f"Serving on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run() 