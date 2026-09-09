from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.agent import run_agent
from app.agent.graph import agent_graph, LANGGRAPH_AVAILABLE
from app.agent.memory import save_turn, get_recent_turns

router = APIRouter()


class AgentRequest(BaseModel):
    message: str
    session_id: str = "default"


@router.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    history = await get_recent_turns(request.session_id)
    result = await run_agent(request.message, history=history)
    await save_turn(request.session_id, "user", request.message)
    await save_turn(request.session_id, "assistant", result["answer"])
    return result


@router.post("/agent/workflow")
async def agent_workflow(request: AgentRequest):
    if not LANGGRAPH_AVAILABLE or agent_graph is None:
        raise HTTPException(
            status_code=503,
            detail="LangGraph workflow is not available. Install the 'langgraph' package to enable this endpoint."
        )
    result = await agent_graph.ainvoke({"query": request.message, "route": None, "tool_result": None, "answer": None})
    return {"answer": result["answer"]}