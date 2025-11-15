from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Celestial AI Render is running!"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/command")
def command(cmd: str = "none"):
    return {
        "received": cmd,
        "response": "Thiên Đạo nhận lệnh: " + cmd
    }
