from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "msg": "Thien Dao AI Live"}

class Event(BaseModel):
    player: str
    action: str
    data: dict | None = None

@app.post("/mc/event")
def mc_event(evt: Event):
    return {"received": evt}
