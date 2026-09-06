from app.services.llm.factory import get_llm_client

SUMMARY_PROMPT = """You are summarizing a medical lab report for a patient, based ONLY on the structured test data below. Do not add any medical knowledge, diagnosis, or interpretation beyond what is directly supported by this data.

Test data (JSON):
{tests_json}

Write a summary with exactly these five sections, using these exact headers:

Report Overview
(1-2 sentences: what kind of tests this report contains, and how many were found)

Key Findings
(A short bulleted list of the tests and their values)

Values Outside Reported Range
(List any tests with status "high" or "low", referencing the range that was printed on the report. If none, say "No values were flagged as outside the reported range.")

Important Changes
(Say: "This summary is based on a single report and does not include comparisons across time." Do not speculate about trends.)

Questions to Discuss With a Healthcare Professional
(2-4 neutral, non-alarming questions the patient could ask their doctor about these specific results)

Rules:
- Never diagnose any condition.
- Never recommend starting, stopping, or changing medication.
- Never state a value is dangerous or safe — only state whether it is inside or outside the reported range.
- Do not invent any test, value, or range not present in the data above.
"""


def generate_report_summary(tests: list[dict]) -> str:
    if not tests:
        return (
            "Report Overview\nNo structured test data was found in this report.\n\n"
            "This document may not contain lab test results, or the text could not be extracted."
        )

    import json
    tests_json = json.dumps(tests, indent=2)
    prompt = SUMMARY_PROMPT.format(tests_json=tests_json)

    client = get_llm_client()
    return client.generate(prompt)