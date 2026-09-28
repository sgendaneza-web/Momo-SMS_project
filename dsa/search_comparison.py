import json
import time
import random

def load_transactions(json_path="transactions.json") -> list:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def linear_search(transactions: list, target_id: int):
    """
    O(n) — scans the list one record at a time until it finds a
    matching id, or reaches the end.
    """
    for txn in transactions:
        if txn["id"] == target_id:
            return txn
    return None


def build_lookup_dict(transactions: list) -> dict:
    """
    Converts the list into a dictionary keyed by id, so lookups
    become O(1) average case instead of O(n).
    """
    return {txn["id"]: txn for txn in transactions}


def dict_lookup(lookup: dict, target_id: int):
    return lookup.get(target_id)


def time_linear_search(transactions: list, ids_to_find: list) -> float:
    start = time.perf_counter()
    for target_id in ids_to_find:
        linear_search(transactions, target_id)
    return time.perf_counter() - start


def time_dict_lookup(lookup: dict, ids_to_find: list) -> float:
    start = time.perf_counter()
    for target_id in ids_to_find:
        dict_lookup(lookup, target_id)
    return time.perf_counter() - start


def run_comparison(all_transactions: list, sample_size: int, searches_per_run: int = 500):
    """
    Takes the first `sample_size` transactions, builds both data
    structures, and times `searches_per_run` random ID lookups
    against each.
    """
    subset = all_transactions[:sample_size]
    lookup_dict = build_lookup_dict(subset)

    # Pick random existing IDs to search for, repeated to get a
    # measurable total time even on tiny datasets.
    ids_to_find = [random.choice(subset)["id"] for _ in range(searches_per_run)]

    linear_time = time_linear_search(subset, ids_to_find)
    dict_time = time_dict_lookup(lookup_dict, ids_to_find)

    print(f"\n--- Dataset size: {sample_size} records ({searches_per_run} lookups) ---")
    print(f"Linear search total time:   {linear_time:.6f} sec")
    print(f"Dictionary lookup total time: {dict_time:.6f} sec")
    if dict_time > 0:
        print(f"Dictionary lookup is ~{linear_time / dict_time:.1f}x faster")


if __name__ == "__main__":
    all_transactions = load_transactions()
    max_available = len(all_transactions)
    print(f"Loaded {max_available} transactions from transactions.json")

    for size in [20, 100, 1000]:
        if size > max_available:
            print(f"\nSkipping size {size} — only {max_available} records available.")
            print("(You can duplicate/synthesize extra records if you need larger sizes for the report.)")
            continue
        run_comparison(all_transactions, size)
