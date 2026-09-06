import re
from app.db.database import database

collection = database["documents"]


def _parse_numeric(value: str) -> float | None:
    match = re.search(r"-?\d+\.?\d*", value.replace(",", ""))
    return float(match.group()) if match else None


async def get_test_history(test_name: str) -> list[dict]:
    history = []
    async for doc in collection.find({"tests.test_name": {"$regex": f"^{re.escape(test_name)}$", "$options": "i"}}):
        for test in doc.get("tests", []):
            if test["test_name"].lower() == test_name.lower():
                history.append({
                    "document_id": str(doc["_id"]),
                    "filename": doc["filename"],
                    "uploaded_at": doc["uploaded_at"],
                    "value": test["value"],
                    "unit": test.get("unit"),
                    "reference_range": test.get("reference_range"),
                    "status": test["status"],
                })
    history.sort(key=lambda x: x["uploaded_at"])
    return history


async def compare_test(test_name: str) -> dict:
    history = await get_test_history(test_name)
    comparisons = []
    for i in range(1, len(history)):
        prev, curr = history[i - 1], history[i]
        prev_val, curr_val = _parse_numeric(prev["value"]), _parse_numeric(curr["value"])
        diff = None
        if prev_val is not None and curr_val is not None:
            diff = round(curr_val - prev_val, 2)
        comparisons.append({
            "from": prev,
            "to": curr,
            "difference": diff,
        })
    return {"test_name": test_name, "history": history, "comparisons": comparisons}