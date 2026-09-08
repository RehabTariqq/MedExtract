import json
from openai import OpenAI
from app.core.config import OPENAI_API_KEY
from app.agent.tools import TOOL_DEFINITIONS, execute_tool

_client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are MedExtract's assistant. You help users understand their medical reports
using the tools available to you. You must use tool results exactly as returned — never invent
numbers, dates, or values. If a tool returns no data, say so plainly. Never diagnose or recommend
treatment changes."""


async def run_agent(user_message: str, history: list[dict] | None = None) -> dict:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOL_DEFINITIONS,
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            try:
                result = await execute_tool(tool_call.function.name, args)
            except Exception as e:
                result = {"error": str(e)}
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

        final_response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        final_text = final_response.choices[0].message.content
    else:
        final_text = message.content

    return {"answer": final_text}