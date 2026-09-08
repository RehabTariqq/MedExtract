from app.services import search_service, comparison_service, rag_service, summary_service, document_service

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search the user's documents by keyword or topic",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_test_history",
            "description": "Get the full history of a specific test across all reports",
            "parameters": {
                "type": "object",
                "properties": {"test_name": {"type": "string"}},
                "required": ["test_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_reports",
            "description": "Compare a specific test's values across all reports over time",
            "parameters": {
                "type": "object",
                "properties": {"test_name": {"type": "string"}},
                "required": ["test_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_evidence",
            "description": "Ask a grounded question across all documents and get an answer with sources",
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"],
            },
        },
    },
]


async def execute_tool(name: str, arguments: dict) -> dict:
    if name == "search_documents":
        return await search_service.combined_search(arguments["query"])
    if name == "get_test_history":
        return await comparison_service.get_test_history(arguments["test_name"])
    if name == "compare_reports":
        return await comparison_service.compare_test(arguments["test_name"])
    if name == "search_evidence":
        return rag_service.answer_question(arguments["question"])
    return {"error": f"Unknown tool: {name}"}