from fastapi import FastAPI, Request
from _utils import init_csv_file, save_message_to_csv, extract_coordinates
import uvicorn

app = FastAPI()


# === Telegram Webhook Endpoint ===
@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    message = payload.get("message")

    if message:
        lat,lon = extract_coordinates(message)
        save_message_to_csv(message, lat, lon)

    return {"ok": True}


# === Run server directly ===
if __name__ == "__main__":
    
    init_csv_file()  # Set up CSV before starting the server
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)