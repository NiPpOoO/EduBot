import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agent import create_hermes_agent
from tools.wiki_tool import WikiTool
from tools.youtube_tool import YouTubeTool

load_dotenv()
app = FastAPI(title="HermesEduBot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация агента
tools = [WikiTool(), YouTubeTool()]
agent_executor = create_hermes_agent(tools)

@app.post("/chat")
async def chat_endpoint(message: dict):
    """API для чата"""
    user_query = message.get("query")
    response = agent_executor.invoke({"messages": [{"role": "user", "content": user_query}]})
    return {"response": response["messages"][-1]["content"]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket для realtime чата"""
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = agent_executor.invoke({"messages": [{"role": "user", "content": data}]})
        await websocket.send_text(result["messages"][-1]["content"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
