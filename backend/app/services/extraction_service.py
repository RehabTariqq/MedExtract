import json
import logging
import re

from pydantic import ValidationError

from app.schemas.medical_test import MedicalTest
from app.services.llm.factory import get_llm_client

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """You are extracting structured data from a medical lab report page.

Read the text below and identify every test result mentioned. For each one, extract:
- test_name: the name of the test (e.g. "Hemoglobin")
- value: the measured value, as printed (e.g. "13.5")
- unit: the unit, as printed (e.g. "g/dL"), or null if not present
- reference_range: the reference/normal range AS PRINTED IN THIS REPORT (e.g. "12.0-15.5"), or null if not present
- status: "normal", "high", "low", or "unclear" based on comparing the value to the reference range printed in THIS report. If no range is given, use "unclear".
- category: a general category if identifiable (e.g. "Hematology", "Metabolic"), or null
- source_text: the exact line/snippet from the text that this was extracted from

Rules:
- Only extract values that are explicitly present in the text below. Do not infer or invent any test, value, or range.
- If the text contains no lab test results, return an empty list.
- Base "status" only on the reference range printed in this specific text, never on general medical knowledge.

Return ONLY valid JSON matching this exact shape, with no other text, no markdown code fences:
{{"tests": [{{"test_name": "...", "value": "...", "unit": "...", "reference_range": "...", "status": "...", "category": "...", "source_text": "..."}}]}}

Page text:
---
{page_text}
---
"""


def _parse_json_loosely(raw: str):
    """Pull a JSON object/array out of an LLM reply, tolerating fences and chatter."""
    if not raw:
        raise ValueError("empty LLM response")
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end > start:
        return json.loads(cleaned[start : end + 1])
    raise ValueError("no JSON object found in LLM response")


def extract_tests_from_page(page_text: str, page_number: int) -> list[dict]:
    if not page_text or not page_text.strip():
        return []

    client = get_llm_client()
    prompt = EXTRACTION_PROMPT.format(page_text=page_text)

    # LLM/API errors are allowed to propagate so the upload is marked "failed"
    # with a real reason instead of silently producing zero tests.
    raw_response = client.generate(prompt)

    try:
        parsed = _parse_json_loosely(raw_response)
    except (ValueError, json.JSONDecodeError) as e:
        logger.warning("Page %s: could not parse LLM JSON (%s). Raw: %.300s", page_number, e, raw_response)
        return []

    items = parsed.get("tests", []) if isinstance(parsed, dict) else parsed
    if not isinstance(items, list):
        return []

    tests: list[dict] = []
    for item in items:
        try:
            test = MedicalTest(**item)  # validate each test on its own
        except (ValidationError, TypeError) as e:
            logger.warning("Page %s: skipped invalid test %s (%s)", page_number, item, e)
            continue
        d = test.model_dump()
        d["page_number"] = page_number
        tests.append(d)
    return tests
