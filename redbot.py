import discord
from discord.ext import commands
import os

# Your original bot setup
intents = discord.Intents.default()
intents.reactions = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # Needed to read messages

bot = commands.Bot(command_prefix="!", intents=intents)

# Your constants
YOUR_USER_ID = 649851863109468171
CHANNEL_ID = 875804404182286387
KARUTA_BOT_ID = 646937666251915264
SAFE_EMOJIS = ["1️⃣", "2️⃣", "3️⃣"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message

    if message.channel.id == CHANNEL_ID and message.author.id == KARUTA_BOT_ID:
        emoji = str(reaction.emoji)
        if emoji not in SAFE_EMOJIS:
            channel = bot.get_channel(CHANNEL_ID)

            try:
                target_user = await bot.fetch_user(YOUR_USER_ID)
                await target_user.send(
                    f"🚨 Special emoji reaction detected: **{emoji}** in {channel.mention}!"
                )
            except Exception as e:
                print(f"Failed to DM: {e}")

            try:
                await channel.send(
                    f"<@{YOUR_USER_ID}> 🍉 Special emoji dropped: **{emoji}**"
                )
            except Exception as e:
                print(f"Failed to ping in channel: {e}")

# 👇 Run your bot using the token from environment variable
bot.run(os.environ['token'])
