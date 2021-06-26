'  Importing from config.py  '
from config import *

class basic(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed=discord.Embed(title="Toad Sings Help Commands", color=0x680af5)
        embed.add_field(name="/join", value="Toad Sings joins the current voice call as you are.", inline=True)
        embed.add_field(name="/play *Insert YouTube Link*", value="Toad Sings plays the youtube link that has been given. Toad Sings only supports Youtube currently. Youtube titles Won't work. It **Must** be links. ", inline=False)
        embed.add_field(name="/dc", value="Toad Sings disconnects from current voice call.", inline=False)
        embed.add_field(name="/pause", value="Toad Sings will pause the current song playing.", inline=False)
        embed.add_field(name="/resume", value="Toad Sings will resume the current song playing.", inline=False)
        embed.add_field(name="/stop", value="Toad Sings will stop or delete the current song/playlist", inline=False)
        embed.add_field(name="/queue *Insert YouTube Link*", value="Toad Sings will play the Youtube Link provided by you. **No other providers are supported.**", inline=False)
        embed.add_field(name="/skip", value="Toad Sings will skip the current song from being played.", inline=False)
        await ctx.send(embed=embed)
    

def setup(client):
    client.add_cog(basic(client))