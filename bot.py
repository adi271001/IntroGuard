import discord
import os
from discord.ext import commands

# Enable intents with message content access
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# List of allowed channel IDs where deletion is skipped (put your actual allowed channel IDs here)
ALLOWED_CHANNELS = [1446493163731550330, 1448260506031882373]  # e.g. [123456789012345678]

INTRO_THRESHOLD = 0.1  # Dummy threshold for demo

HELP_KEYWORDS = [
    "issue", "problem", "error", "bug", "failing",
    "doesn't work", "cant sign", "can't sign",
    "not working", "404", "500", "api",
    "anyone facing", "anyone else"
]

def is_help_message(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in HELP_KEYWORDS)

def intro_score(text: str) -> float:
    # Dummy scoring: treat any message containing 'intro' as intro-like
    text = text.lower()
    intro_keywords = [
        "i am", "i'm", "hello", "hi", "developer", "dev", "open to collab",
        "looking for", "resume", "bio", "introduce myself", "available for"
    ]
    hits = sum(word in text for word in intro_keywords)
    return hits / len(intro_keywords)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    print(f"[MSG] From {message.author}: {message.content}")

    if is_help_message(message.content):
        print("[INFO] Help message detected, skipping deletion.")
        await bot.process_commands(message)
        return

    score = intro_score(message.content)
    print(f"[INFO] Intro score: {score}")

    if score >= INTRO_THRESHOLD and message.channel.id not in ALLOWED_CHANNELS:
        try:
            await message.delete()
            print(f"[ACTION] Deleted message from {message.author} in channel {message.channel}")
        except Exception as e:
            print(f"[ERROR] Could not delete message: {e}")

    await bot.process_commands(message)

@bot.command()
async def deltest(ctx):
    """Command to test message deletion"""
    try:
        await ctx.message.delete()
        await ctx.send("Deleted your command message!")
    except Exception as e:
        await ctx.send(f"Delete failed: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))

