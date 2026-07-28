import os
import subprocess
import discord
from discord.ext import commands

# 1. Setup intents (required to read messages and commands)
intents = discord.Intents.default()
intents.message_content = True

# 2. Define the command prefix (e.g., !hello, !status)
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Prints to the Pi terminal when the bot successfully connects
@bot.event
async def on_ready():
    print(f"----------------------------------------")
    print(f"Success! Bot is online.")
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print(f"----------------------------------------")

# Command 1: A simple conversational response
@bot.command(name="hello")
async def hello_command(ctx):
    """Replies with a greeting and greets the user by name."""
    await ctx.send(f"Hello {ctx.author.mention}! I am online and listening from your Raspberry Pi.")

# Command 2: Checks the Pi's internal temperature
@bot.command(name="status")
async def status_command(ctx):
    """Fetches the current CPU temperature of the Raspberry Pi."""
    try:
        # Runs the Pi hardware command to get temperature
        cmd = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
        temp = cmd.stdout.strip().replace("temp=", "")
        await ctx.send(f"📊 **Pi Status:**\n🌡️ CPU Temperature: `{temp}`")
    except Exception as e:
        await ctx.send("❌ Could not read system temperature. Am I running on a Linux/Pi system?")

# Command 3: Safely shuts down the Pi remotely
@bot.command(name="shutdown")
@commands.is_owner() # Ensures ONLY you (the application creator) can run this
async def shutdown_command(ctx):
    """Safely powers off the Raspberry Pi."""
    await ctx.send("🔌 Shutting down the Raspberry Pi now. Goodbye!")
    os.system("sudo shutdown -h now")

# Error handler for the shutdown command if someone else tries to use it
@shutdown_command.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("⛔ You do not have permission to shut down this Raspberry Pi.")

# 3. Start the bot (Replace with your actual token)
bot.run("YOUR_DISCORD_BOT_TOKEN_HERE")
