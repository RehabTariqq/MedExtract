from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import run_agent
from app.agent.graph import agent_graph

router = APIRouter()


class AgentRequest(BaseModel):
    message: str


@router.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    return await run_agent(request.message)


@router.post("/agent/workflow")
async def agent_workflow(request: AgentRequest):
    result = await agent_graph.ainvoke({"query": request.message, "route": None, "tool_result": None, "answer": None})
    return {"answer": result["answer"]}