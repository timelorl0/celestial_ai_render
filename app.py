from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
import time

app = FastAPI(title="Celestial AI – Thien Dao Core")

# ====== DATA MODEL TỪ FALIX GỬI SANG ======

class Event(BaseModel):
    event: str            # "player_join", "tick", "chat", ...
    player: str | None = None
    world: str | None = None
    payload: Dict[str, Any] = {}

class Action(BaseModel):
    type: str             # "message", "title", "command", "effect"
    target: str | None = None
    data: Dict[str, Any] = {}

class Response(BaseModel):
    ok: bool
    actions: List[Action] = []
    meta: Dict[str, Any] = {}

# ====== “BỘ NÃO THIÊN ĐẠO” CỰC GỌN ======

def handle_event(ev: Event) -> Response:
    actions: List[Action] = []

    # Ví dụ: chào khi người chơi join
    if ev.event == "player_join" and ev.player:
        actions.append(Action(
            type="message",
            target=ev.player,
            data={
                "text": f"Chào {ev.player}, ngươi đã bước vào Hư Không Tuyệt Đối.",
                "color": "gold"
            }
        ))
        actions.append(Action(
            type="title",
            target=ev.player,
            data={
                "title": "§5Thiên Đạo đang quan sát...",
                "subtitle": "§7Vũ trụ sẽ hiện hình theo tâm niệm của ngươi."
            }
        ))

    # Tick định kỳ – sau này ta sẽ dùng để cho vũ trụ “tự vận hành”
    if ev.event == "tick":
        # Ở đây mình chỉ trả meta đơn giản.
        return Response(
            ok=True,
            actions=[],
            meta={"status": "alive", "ts": time.time()}
        )

    # Chat – sau này có thể làm AI trả lời chat
    if ev.event == "player_chat" and ev.player:
        msg = str(ev.payload.get("message", "")).lower()
        if "thiên đạo" in msg:
            actions.append(Action(
                type="message",
                target=ev.player,
                data={
                    "text": "Thiên Đạo: Ta đang lắng nghe.",
                    "color": "dark_purple"
                }
            ))

    return Response(ok=True, actions=actions, meta={"ts": time.time()})


# ====== API CHÍNH THIÊN ĐẠO ======

@app.post("/api/celestial", response_model=Response)
async def celestial_endpoint(ev: Event):
    """
    Falix gọi POST /api/celestial với JSON Event
    Thiên Đạo trả về danh sách Action.
    """
    try:
        resp = handle_event(ev)
        return resp
    except Exception as e:
        return Response(ok=False, actions=[], meta={"error": str(e)})


@app.get("/")
def root():
    return {"status": "ok", "msg": "Celestial AI – Thien Dao is running."}