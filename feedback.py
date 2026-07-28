import discord
from discord.ext import commands

# 1. CONFIGURE GATEWAY INTENTS
# Message content intent must be enabled to read the text inside messages
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. CONFIGURATION VARIABLES
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
FEEDBACK_CHANNEL_ID = 123456789012345678  # Replace with your actual Channel ID

@bot.event
async def on_ready():
    print(f"Bot logged in as: {bot.user}")
    print("Now listening for server feedback on your Raspberry Pi...")

@bot.event
async def on_message(message):
    # Ignore messages sent by bots to prevent feedback loops
    if message.author.bot:
        return

    # Check if the message was sent inside your designated feedback channel
    if message.channel.id == FEEDBACK_CHANNEL_ID:
        
        # Capture the feedback text and user metadata
        user_name = message.author.name
        feedback_content = message.content
        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # Print directly to your Thonny IDE console window
        print(f"\n📥 [NEW FEEDBACK] {timestamp}")
        print(f"From: {user_name}")
        print(f"Message: {feedback_content}")
        print("-" * 40)
        
        # Optional: Append the feedback to a local text file on your Pi
        with open("server_feedback.txt", "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {user_name}: {feedback_content}\n")

    # Keep command processing active for other bot tasks
    await bot.process_commands(message)

# 3. RUN THE BOT
bot.run(BOT_TOKEN)
