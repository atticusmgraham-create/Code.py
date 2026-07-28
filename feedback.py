from fastapi import FastAPI, Request, HTTPException
from discord_interactions import verify_key_cb

app = FastAPI()

# Get this string from the "General Information" tab of the Discord Developer Portal
DISCORD_PUBLIC_KEY = "YOUR_BOT_PUBLIC_KEY_HERE"

@app.post("/webhook")
async def discord_webhook(request: Request):
    # 1. Verify that the request actually came from Discord security systems
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()
    
    if not signature or not timestamp or not verify_key_cb(body, signature, timestamp, DISCORD_PUBLIC_KEY):
        raise HTTPException(status_code=401, detail="Invalid request signature")

    # 2. Parse the feedback data
    data = await request.json()
    
    # Handle Discord's initial system handshake (Type 1 is a PING)
    if data.get("type") == 1:
        return {"type": 1}
        
    # Handle Form/Modal submissions (Type 5)
    if data.get("type") == 5:
        # Extract the text the user typed into the form
        components = data["data"]["components"]
        user_feedback = components[0]["components"][0]["value"]
        user_name = data["member"]["user"]["username"]
        
        # PROCESS YOUR FEEDBACK HERE (e.g., save to database, print log)
        print(f"Feedback from {user_name}: {user_feedback}")
        
        # Tell the user Discord successfully recorded their entry
        return {
            "type": 4, # Response type to show a message
            "data": {
                "flags": 64, # Ephemeral flag (only the user who clicked can see this message)
                "content": "Thank you! Your feedback has been submitted successfully."
            }
        }

    return {"status": "unhandled interaction type"}
