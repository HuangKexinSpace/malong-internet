# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import Optional

app = FastAPI()

# 开启 CORS，允许 Web 端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    command: str

# 全局缓存当前命令，并发保护
_current_command: Optional[str] = None
_lock = asyncio.Lock()

@app.post("/send_command")
async def send_command(cmd: Command):
    global _current_command
    async with _lock:
        _current_command = cmd.command
    return {"status": "ok"}

@app.get("/get_command")
async def get_command():
    global _current_command
    async with _lock:
        cmd = _current_command
        _current_command = None  # 取出后清空
    return {"command": cmd}

# uvicorn main:app --reload --host 0.0.0.0 --port 8000
# uvicorn main:app --host 0.0.0.0 --port 8000
# uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem