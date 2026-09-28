"""
parse_xml.py
Parses modified_sms_v2.xml (MTN MoMo SMS backup) into a list of
transaction dictionaries and saves them as transactions.json.
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime


# ---------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------
def to_number(text):
    """'2,000' -> 2000 ; None -> None. Returns int when whole, else float."""
    if text is None:
        return None
    value = float(text.replace(",", ""))
    return int(value) if value.is_integer() else value


def first_match(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    return m.group(1) if m else None


# ---------------------------------------------------------------
# Classification: which kind of message is this?
# Order matters: more specific checks come first.
# ---------------------------------------------------------------
def classify(body: str) -> str:
    if "one-time password" in body:
        return "otp"
    if "reversal has been initiated" in body or "has been reversed" in body:
        return "reversal"
    if re.search(r"\bfailed at\b", body):
        return "failed"
    if "bank deposit of" in body or re.search(r"\bDEPOSIT RWF\b", body):
        return "bank_deposit"
    if "withdrawn" in body:
        return "withdrawal"
    if body.lstrip().startswith("Yello!Umaze kugura"):
        return "bundle_purchase"
    if re.search(r"Y'ello,\s*A transaction of", body):
        return "merchant_payment"          
    if "Your payment of" in body:
        return "payment"                   
    if "transferred" in body:
        return "transfer"
    if "You have received" in body:
        return "received"
    return "other"


# ---------------------------------------------------------------
# Field extractors (each works on the SMS body text)
# ---------------------------------------------------------------
def extract_amount(body):
    patterns = [
        r"Your payment of ([\d,]+) RWF",
        r"You have received ([\d,]+) RWF",
        r"([\d,]+) RWF transferred",
        r"You have transferred ([\d,]+) RWF",
        r"bank deposit of ([\d,]+) RWF",
        r"A transaction of ([\d,]+) RWF",
        r"withdrawn ([\d,]+) RWF",
        r"transaction with amount ([\d,]+) RWF",
        r"DEPOSIT RWF ([\d,]+)",
        r"igura ([\d,]+) RWF",              # bundle purchases
        r"with ([\d,]+) RWF",               # reversals
    ]
    for p in patterns:
        val = first_match(p, body)
        if val:
            return to_number(val)
    return None


def extract_fee(body):
    return to_number(first_match(r"Fee was:?\s*([\d,]+)\s*RWF", body))


def extract_balance(body):
    return to_number(
        first_match(r"(?:new balance|NEW BALANCE)\s*(?:is)?\s*:?\s*([\d,]+)\s*RWF", body, re.I)
    )


def extract_txn_id(body):
    return (
        first_match(r"Financial Transaction Id:\s*(\d+)", body)
        or first_match(r"TxId:\s*(\d+)", body)
    )


def extract_body_timestamp(body):
    """The transaction time written inside the SMS text, e.g. 2024-05-10 16:30:51."""
    return first_match(r"(\d{4}-\d{2}-\d{2}[ ]\d{2}:\d{2}:\d{2})", body)


def extract_counterparty(body, tx_type):
    """Returns (name, phone) for the other party, or None values when absent."""
    name = None
    if tx_type == "received":
        name = first_match(r"received [\d,]+ RWF from (.+?) \(", body)
    elif tx_type == "payment":
        name = first_match(r"Your payment of [\d,]+ RWF to (.+?) (?:\(?\d+\)?\s)?has been completed", body)
    elif tx_type == "transfer":
        name = (first_match(r"[\d,]+ RWF transferred to (.+?) \(", body)
                or first_match(r"You have transferred [\d,]+ RWF to (.+?) \(", body))
    elif tx_type == "merchant_payment":
        name = first_match(r"A transaction of [\d,]+ RWF by (.+?)\s+on your MOMO", body)
    elif tx_type == "withdrawal":
        name = first_match(r"via agent:\s*(.+?) \(", body)
    elif tx_type == "reversal":
        name = first_match(r"transaction to (.+?) \(", body)
    elif tx_type == "failed":
        name = first_match(r"for (.+?) with message", body)

    if name:
        name = re.sub(r"\s+", " ", name).strip()
        name = re.sub(r"\s+\d+$", "", name)   # "Jane Smith 12845" -> "Jane Smith"

    phone = first_match(r"\((\*{0,9}\d{3,12})\)", body)
    return (name or None), phone


# ---------------------------------------------------------------
# Main parsing function
# ---------------------------------------------------------------
def parse_sms_xml(xml_path: str) -> list:
    root = ET.parse(xml_path).getroot()
    records = []

    for idx, sms in enumerate(root.findall("sms"), start=1):
        body = sms.get("body", "")
        tx_type = classify(body)
        name, phone = extract_counterparty(body, tx_type)

        body_ts = extract_body_timestamp(body)
        epoch_ms = int(sms.get("date", "0"))
        # Prefer the time written in the message; fall back to the phone's receive time.
        timestamp = (body_ts.replace(" ", "T") if body_ts else
                     datetime.fromtimestamp(epoch_ms / 1000).strftime("%Y-%m-%dT%H:%M:%S"))

        records.append({
            "id": idx,
            "transaction_type": tx_type,
            "amount": extract_amount(body),
            "fee": extract_fee(body),
            "new_balance": extract_balance(body),
            "counterparty": name,
            "counterparty_phone": phone,
            "financial_transaction_id": extract_txn_id(body),
            "timestamp": timestamp,
            "raw_body": body,
        })
    return records


def save_as_json(records: list, output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    input_xml = os.path.join(here, "modified_sms_v2.xml")
    output_json = os.path.join(here, "transactions.json")

    if not os.path.exists(input_xml):
        raise SystemExit(f"Could not find {input_xml}. Put modified_sms_v2.xml in the dsa/ folder.")

    data = parse_sms_xml(input_xml)
    save_as_json(data, output_json)

    print(f"Parsed {len(data)} SMS records -> {output_json}")
    counts = {}
    for r in data:
        counts[r["transaction_type"]] = counts.get(r["transaction_type"], 0) + 1
    for t, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {t:18} {n}")
    print("\nSample record:")
    print(json.dumps(data[0], indent=2, ensure_ascii=False))