import discord
from discord.ext import commands

# 👇 For uptime (optional with Railway/Render)
from flask import Flask
from threading import Thread
import os

# 👇 Minimal keep-alive web server
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 👇 Start Flask web server (optional)
keep_alive()

# 👇 Intents setup
intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # Needed to read message content

bot = commands.Bot(command_prefix="!", intents=intents)

# 👇 Your constants
YOUR_USER_ID = 649851863109468171  # Your Discord ID
CHANNEL_ID = 875804404182286387    # Karuta drop channel
KARUTA_BOT_ID = 646937666251915264  # Karuta bot's ID

SAFE_EMOJIS = ["1️⃣", "2️⃣", "3️⃣"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message

    # Only handle Karuta bot messages in the specified channel
    if message.channel.id == CHANNEL_ID and message.author.id == KARUTA_BOT_ID:
        emoji = str(reaction.emoji)
        if emoji not in SAFE_EMOJIS:
            channel = bot.get_channel(CHANNEL_ID)

            # Try to DM you
            try:
                target_user = await bot.fetch_user(YOUR_USER_ID)
                await target_user.send(
                    f"🚨 Special emoji reaction detected: **{emoji}** in {channel.mention}!"
                )
            except Exception as e:
                print(f"❌ Failed to DM: {e}")

            # Try to ping you in the channel
            try:
                await channel.send(f"<@{YOUR_USER_ID}> 🍉 Special emoji dropped: **{emoji}**")
            except Exception as e:
                print(f"❌ Failed to ping in channel: {e}")

# 👇 Secure way to load your bot token
DISCORD_TOKEN = os.environ.get("TOKEN")

if not DISCORD_TOKEN:
    raise Exception("❌ TOKEN environment variable not set!")

bot.run(DISCORD_TOKEN)
