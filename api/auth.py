import base64
import hmac
import os
 
VALID_USERNAME = os.environ.get("MOMO_USERNAME", "admin")
VALID_PASSWORD = os.environ.get("MOMO_PASSWORD", "momo123")
 
 
def check_auth(auth_header: str) -> bool:
    if not auth_header or not auth_header.startswith("Basic "):
        return False
 
    encoded_credentials = auth_header.split(" ", 1)[1]
 
    try:
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":", 1)
    except Exception:
        return False
 
    username_ok = hmac.compare_digest(
        username.encode("utf-8"), VALID_USERNAME.encode("utf-8")
    )
    password_ok = hmac.compare_digest(
        password.encode("utf-8"), VALID_PASSWORD.encode("utf-8")
    )
    return username_ok and password_ok
 
 
def build_401_body() -> dict:
    return {"error": "Unauthorized", "message": "Valid Basic Auth credentials required."}
 