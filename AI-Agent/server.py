from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import Agent

app = FastAPI(title="AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Single agent instance per server session
agent = Agent()

class ChatRequest(BaseModel):
    message: str

class ResetRequest(BaseModel):
    pass

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response, tools_used = agent.chat(req.message)
        return {
            "response": response,
            "tools_used": tools_used,
            "tool_calls_total": agent.tool_calls_made,
            "history_length": len([m for m in agent.history if m["role"] != "system"])
        }
    except Exception as e:
        return {"error": str(e), "response": f"Error: {str(e)}", "tools_used": []}

@app.post("/reset")
def reset():
    agent.reset()
    return {"message": "Conversation reset"}

@app.get("/tools")
def list_tools():
    from tools import TOOL_SCHEMAS
    return {"tools": [t["function"]["name"] for t in TOOL_SCHEMAS]}

@app.get("/stats")
def stats():
    return {
        "tool_calls_made": agent.tool_calls_made,
        "history_length": len([m for m in agent.history if m["role"] != "system"]),
        "model": agent.model
    }
