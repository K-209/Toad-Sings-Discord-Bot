from config import *


if os.path.exists(os.getcwd() + "/data/config.json"):
    with open("./data/config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "?"}
    with open(os.getcwd() + "/data/config.json", "w+") as f:
        json.dump(configTemplate, f)

TOKEN = configData["Token"]
BOT_PREFIX = configData["Prefix"]

client = commands.Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("?help | Working Carefully"))
    print("Logged in as: " + client.user.name + "\n")

@client.command(aliases=["refresh"])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"{client.user.name} has reloaded the cog!")

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Successfully loaded!")
    await ctx.send(f"{client.user.name} has loaded the cog!")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"{client.user.name} has unloaded the cog!")

client.run(TOKEN)
