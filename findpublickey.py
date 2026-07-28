import requests

# Replace these with your actual credentials from the Developer Portal
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
APPLICATION_ID = "YOUR_APPLICATION_ID_HERE"

url = f"https://discord.com{APPLICATION_ID}/commands"

headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Define the command and the text input field
command_data = {
    "name": "feedback",
    "description": "Submit your feedback directly from this text channel",
    "options": [
        {
            "name": "message",
            "description": "Type your feedback here",
            "type": 3,  # Type 3 represents a text string input
            "required": True
        }
    ]
}

response = requests.post(url, headers=headers, json=command_data)
print(response.json())  # Should output the registered command details
