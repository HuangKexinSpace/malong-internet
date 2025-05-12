# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# 1. CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 或 ["https://aidealmalong.zeabur.app"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 命令模型 & 存储
class Command(BaseModel):
    command: str

_current_command: str | None = None

# 3. 接收命令
@app.post("/send_command")
async def send_command(cmd: Command):
    global _current_command
    _current_command = cmd.command
    return {"status": "ok"}

# 4. 获取命令
@app.get("/get_command")
async def get_command():
    global _current_command
    cmd = _current_command
    _current_command = None
    return {"command": cmd}

# 5. 挂载静态目录 —— 根目录下所有文件均可访问，html=True 使 / 返回 index.html
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# 6. 本地调试用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)