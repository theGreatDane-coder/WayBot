## ⚡️ Quick Start: Run the Bot in 3 Commands

Use these terminal commands to launch your FastAPI server, expose it publicly with ngrok, and connect your Telegram bot to it.

---

### 🔧 Start the FastAPI Server

Make sure you're in the same directory as `server.py`.

```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8000 
```

### 🔥 Expose Your Server with ngrok

Run the following command to expose your local server running on port `8000`:

```bash
ngrok http 8000
```

### 📡 Set Telegram Webhook

Register your bot’s webhook by running:

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_NGROK_URL>/webhook"
```