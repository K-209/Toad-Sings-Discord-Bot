'  Importing from config.py  '
from config import *

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            embed=discord.Embed(title="Hello, I'm Toad Sings!", description=f"My default prefix is `{BOT_PREFIX}`. Hope this helps!", color=0x176cd5)
            await message.reply(embed=embed)

    '  The Errorhandling  '
    @commands.Cog.listener() #Error ignore for MissingPermissions
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return
   
    '  The Errorhandling  '
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.reply(f">>> **I just found an error!**\n{error}")  # Errormessage

def setup(client):
    client.add_cog(events(client))