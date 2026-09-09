from typing import TypedDict, Optional
from app.agent.tools import execute_tool
from app.services.llm.factory import get_llm_client
import json

LANGGRAPH_AVAILABLE = True
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    LANGGRAPH_AVAILABLE = False


class GraphState(TypedDict):
    query: str
    route: Optional[str]
    tool_result: Optional[dict]
    answer: Optional[str]


def route_query(state: GraphState) -> GraphState:
    query_lower = state["query"].lower()
    if "compare" in query_lower or "trend" in query_lower or "history" in query_lower:
        state["route"] = "compare"
    else:
        state["route"] = "evidence"
    return state


async def run_compare(state: GraphState) -> GraphState:
    words = state["query"].split()
    test_name = words[-1]
    result = await execute_tool("compare_reports", {"test_name": test_name})
    state["tool_result"] = result
    return state


async def run_evidence(state: GraphState) -> GraphState:
    result = await execute_tool("search_evidence", {"question": state["query"]})
    state["tool_result"] = result
    return state


def generate_response(state: GraphState) -> GraphState:
    client = get_llm_client()
    prompt = f"""Based on this tool result, answer the user's question concisely and factually.
Never invent data not present in the result.

Question: {state['query']}
Tool result: {json.dumps(state['tool_result'], default=str)}

Answer:"""
    state["answer"] = client.generate(prompt)
    return state


def build_graph():
    if not LANGGRAPH_AVAILABLE:
        return None

    graph = StateGraph(GraphState)
    graph.add_node("route", route_query)
    graph.add_node("compare", run_compare)
    graph.add_node("evidence", run_evidence)
    graph.add_node("respond", generate_response)

    graph.set_entry_point("route")
    graph.add_conditional_edges(
        "route",
        lambda s: s["route"],
        {"compare": "compare", "evidence": "evidence"},
    )
    graph.add_edge("compare", "respond")
    graph.add_edge("evidence", "respond")
    graph.add_edge("respond", END)

    return graph.compile()


agent_graph = build_graph()