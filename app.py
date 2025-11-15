from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal, Dict
from datetime import datetime, timezone

app = FastAPI(title="Celestial AI Render", version="1.0.0")

# ====== MÔ HÌNH DỮ LIỆU ======

class Heartbeat(BaseModel):
    server_id: str
    online_players: int
    tps: float

class RegisterPayload(BaseModel):
    server_id: str
    server_name: str
    motd: str | None = None
    max_players: int | None = None

class Action(BaseModel):
    type: Literal["broadcast", "command"]
    message: str | None = None
    command: str | None = None

# ====== BỘ NHỚ ĐƠN GIẢN TRONG RAM ======

servers: Dict[str, dict] = {}
pending_actions: Dict[str, List[Action]] = {}

# ====== ENDPOINT CƠ BẢN ======

@app.get("/")
async def root():
    return {"status": "ok", "message": "Celestial AI Render is running."}

@app.get("/status")
async def status():
    return {
        "status": "ok",
        "servers": servers,
        "pending_actions": {
            sid: [a.dict() for a in acts]
            for sid, acts in pending_actions.items()
        },
    }

# ====== ĐĂNG KÝ & HEARTBEAT TỪ FALIX ======

@app.post("/mc/register")
async def register(payload: RegisterPayload):
    now = datetime.now(timezone.utc).isoformat()
    servers[payload.server_id] = {
        "name": payload.server_name,
        "motd": payload.motd,
        "max_players": payload.max_players,
        "last_heartbeat": now,
        "online_players": 0,
        "tps": 20.0,
    }
    pending_actions.setdefault(payload.server_id, [])
    return {"ok": True, "registered_at": now}

@app.post("/mc/heartbeat")
async def heartbeat(hb: Heartbeat):
    now = datetime.now(timezone.utc).isoformat()
    info = servers.setdefault(hb.server_id, {})
    info["last_heartbeat"] = now
    info["online_players"] = hb.online_players
    info["tps"] = hb.tps
    return {"ok": True, "updated_at": now}

# ====== HÀNG ĐỢI LỆNH TỪ THIÊN ĐẠO XUỐNG FALIX ======

@app.get("/mc/actions")
async def pull_actions(server_id: str):
    actions = pending_actions.get(server_id, [])
    pending_actions[server_id] = []
    return {
        "ok": True,
        "actions": [a.dict() for a in actions],
    }

# API test: thêm lệnh thủ công cho 1 server
@app.post("/mc/push_action")
async def push_action(server_id: str, action: Action):
    pending_actions.setdefault(server_id, []).append(action)
    return {"ok": True, "queued_for": server_id}
