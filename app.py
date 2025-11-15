from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# -----------------------------
#  CẤU TRÚC TIN NHẮN
# -----------------------------
class Command(BaseModel):
    sender: str
    message: str

# -----------------------------
#  AI THIÊN ĐẠO LOGIC
# -----------------------------
def ai_engine(msg: str):
    msg = msg.lower()

    if "xin chào" in msg or "hello" in msg:
        return "Ta là Thiên Đạo — đã kết nối."
    if "lệnh" in msg:
        return "Thiên Đạo đã nhận lệnh. Đang xử lý..."
    if "status" in msg or "tình trạng" in msg:
        return "Hệ thống Thiên Đạo đang vận hành ổn định."
    
    # fallback
    return f"Thiên Đạo nhận: {msg}"

# -----------------------------
#  API CHÍNH
# -----------------------------
@app.post("/cmd")
async def receive_command(cmd: Command):
    response = ai_engine(cmd.message)
    return {
        "from": "thiendao",
        "to": cmd.sender,
        "response": response
    }

# -----------------------------
#  CHECK SERVER STATUS
# -----------------------------
@app.get("/")
async def root():
    return {"status": "Thiên Đạo đã khởi động thành công!"}

# Chỉ dùng khi chạy LOCAL
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)
