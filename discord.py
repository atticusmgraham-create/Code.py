import discord
import asyncio

# Replace with your actual Bot Token
TOKEN = 'YOUR_BOT_TOKEN_HERE'
# Replace with the numerical ID of your Discord channel
CHANNEL_ID = 123456789012345678 

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_msg():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Hello from Raspberry Pi!")
        print("Message sent successfully.")
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    client.loop.create_task(send_msg())

client.run(TOKEN)
