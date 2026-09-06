import json
import re
from app.services.llm.factory import get_llm_client
from app.schemas.medical_test import ExtractionResult

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


def _clean_json_response(raw: str) -> str:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"```$", "", cleaned)
    return cleaned.strip()


def extract_tests_from_page(page_text: str, page_number: int) -> list[dict]:
    if not page_text.strip():
        return []

    client = get_llm_client()
    prompt = EXTRACTION_PROMPT.format(page_text=page_text)
    raw_response = client.generate(prompt)

    try:
        cleaned = _clean_json_response(raw_response)
        parsed = json.loads(cleaned)
        result = ExtractionResult(**parsed)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Extraction parse error on page {page_number}: {e}")
        return []

    tests = []
    for test in result.tests:
        test_dict = test.model_dump()
        test_dict["page_number"] = page_number
        tests.append(test_dict)
    return tests