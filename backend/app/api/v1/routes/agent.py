from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import run_agent

router = APIRouter()


class AgentRequest(BaseModel):
    message: str


@router.post("/agent/chat")
async def agent_chat(request: AgentRequest):
    return await run_agent(request.message)