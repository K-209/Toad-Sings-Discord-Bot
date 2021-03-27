import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
import shutil
from os import system

TOKEN = "NzE3ODM3NjI0MTczMzk2MDQw.XtgIYg._Lh-xUJqSOrnN5T2wIjTCviZ00I"
BOT_PREFIX = '?'

bot = commands.Bot(command_prefix=BOT_PREFIX)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("?help | Still Beta"))
    print("Logged in as: " + bot.user.name + "\n")

@bot.command(pass_context=True)
async def help(ctx):
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

@bot.command(pass_context=True, aliases=['j', 'Joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, aliases=['dis', 'disconnect'])
async def dc(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Toad has left {channel}")
    else:
        print("Toad thinks you weren't in a voice channel")
        await ctx.send("Toad thinks you weren't in a voice channel")

@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.message.delete()
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued songs(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
            shutil.move(song_path, main_location)
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

            voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1.00

        else:
            queues.clear()
            return

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: Youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '""' + c_path + '""' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.00

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Paused")
        voice.pause()
        await ctx.send("Music Paused")
    else:
        print("Music not playing failed paused")
        await ctx.send("Music not playing failed paused")

@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed Music")
        voice.resume()
        await ctx.send("Music Resumed")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music is playing failed to stop")

queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

    except:
        print("FALLBACK: Youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song {q_num} -f " + '""' + q_path + '""' + " -s " + url)


    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")

@bot.command(pass_context=True, aliases=['sk', 'ski'])
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Skipping current song. Playing next song!")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("ERROR:05B26. Whoops that was not supposed to happen. Please do me a favour and contact the local Developer about this Error.")
        await ctx.send("No music playing failed")


bot.run(TOKEN)
