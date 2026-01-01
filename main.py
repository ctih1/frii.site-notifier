import discord, os, json, traceback
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.presences = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

import json
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

TOKEN = settings["bot"]["token"]
PREFIX = settings["bot"]["prefix"]
MAXWARNS = settings["administration"]["maximum_warnings"]

STATUS = settings["branding"]["status"].lower()
ACTIVITYTYPE = settings["branding"]["activity"]["type"].lower()
ACTIVITY = settings["branding"]["activity"]["content"]

statuses = {
    "online": discord.Status.online,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd,
    "invisible": discord.Status.invisible,
}
activities = {
    "listening": discord.ActivityType.listening,
    "playing": discord.ActivityType.playing,
    "streaming": discord.ActivityType.streaming,
    "competing": discord.ActivityType.competing,
    "watching": discord.ActivityType.watching,
}

async def set_presence(status, act_type, act_name):
    await bot.change_presence(
        status=statuses.get(status.lower(), discord.Status.online),
        activity=discord.Activity(
            type=activities.get(act_type.lower(), discord.ActivityType.unknown),
            name=act_name
        )
    )

async def load_cogs(folder="commands"):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file).replace(os.sep, ".")[:-3]
                try:
                    await bot.load_extension(path)
                    print(f"Loaded: {path}")
                except Exception as e:
                    print(f"Failed: {path} -> {e}")
                    traceback.print_exc()

async def log_command(interaction, event="on_command", error=None, filename=None):
    try:
        cmd_name = interaction.command.name

        data = {
            "type": event,
            "user": str(interaction.user),
            "user_id": interaction.user.id,
            "command": str(cmd_name),
            "time": str(interaction.created_at)
        }

        if error:
            data["error"] = str(error)
            if filename:
                data["file"] = filename

        logs = []
        if os.path.exists("logs.json"):
            try:
                with open("logs.json") as f:
                    logs = json.load(f)
            except json.JSONDecodeError:
                pass

        logs.append(data)

        with open("logs.json", "w") as f:
            json.dump(logs, f, indent=4)
    except Exception:
        pass

@bot.event
async def on_interaction(ctx): await log_command(ctx)

@bot.event
async def on_interaction_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError): error = error.original
    tb = traceback.extract_tb(error.__traceback__) or [("Unknown",0,"Unknown","Unknown")]
    filename, lineno, _, _ = tb[-1]
    await log_command(ctx, "on_command_error", error, f"{filename} Line:{lineno}")
    await ctx.send(embed=discord.Embed(
        title="Error!",
        description=f"{error}\n{filename}\nLine: {lineno}",
        colour=discord.Colour.red()
    ))

@bot.event
async def setup_hook(): 
    await load_cogs()
    try:
        print(f"Syncing slash commands with discord...")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands with discord")
    except Exception as e:
        print(f"An error occured!\n{e}")

@bot.event
async def on_ready():
    await set_presence(STATUS, ACTIVITYTYPE, ACTIVITY)
    print(f'Logged in as {bot.user}')

bot.run(TOKEN)