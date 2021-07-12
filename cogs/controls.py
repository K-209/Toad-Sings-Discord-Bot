'  Importing from config.py  '
from data.config import *

class controls(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['j', 'Joi'])
    async def join(self, ctx):
        '  Join Control Commmand  '
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"Joined {channel}") 

    @commands.command(pass_context=True, aliases=['dis', 'dc'])
    async def disconnect(self, ctx):
        '  Disconnect Control Commmand  '
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(title="Disconnected Successfully", description=f"Toad has left {channel}", color=0x00FF00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error: Cannot Disconnect", description=f"Toad thinks you weren't in a voice channel", color=0xff0000)
            await ctx.send(embed=embed)         

    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):
        '  Pause Control Commmand  '
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Song Paused")
        else:
            await ctx.send("Song was not playing. Pause failed")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        '  Resume Control Commmand  '
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Song has been resumed")
        else:
            await ctx.send("Song is not paused")


def setup(client):
    client.add_cog(controls(client))