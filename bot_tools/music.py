import discord, os, youtube_dl, re
from urllib import parse, request
from discord.ext import commands

song_list = []
global_index = 0

class Music(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def play(self, ctx, *query):
        #check if user and bot is in voice channel
        voiceTrue = ctx.author.voice
        bot = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        try:
            await ctx.author.voice.channel.connect()
        except:
            if voiceTrue is None:
                return await ctx.send("You are not in a voice channel")
            if bot.is_connected():
                return await ctx.send("Bot is already connected to a voice channel")

        #check if mp3 file exists and delete it
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        #modify the user's query so that youtube understands it
        search = ' '.join(list(query))
        print(search)
        search = search.replace(' ','+')
        query_string = parse.urlencode({'search_query': search})
        html = request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall('watch\?v=(.{11})',html.read().decode('utf-8'))
        audio = "https://www.youtube.com/watch?v=" + search_results[0]
        #song_list.append(audio)

        #download the video
        vc = ctx.voice_client
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        #the video is converted to mp3 file
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([audio])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        #the mp3 file is played
        vc.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def leave(self, ctx):
        bot = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if bot.is_connected():
            await bot.disconnect()
        else:
            return await ctx.send("Bot is not connected to a voice channel")

    @commands.command()
    async def pause(self, ctx):
        bot = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if bot.is_playing():
            bot.pause()
            await ctx.send("Music paused")
        else:
            return await ctx.send("Im not playing anything")

    @commands.command()
    async def resume(self, ctx):
        bot = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if bot.is_paused():
            bot.resume()
            await ctx.send("Music resumed")
        else:
            return await ctx.send("Im not paused")

    @commands.command()
    async def stop(self, ctx):
        bot = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if bot.is_playing():
            bot.stop()
            await ctx.send("Music stopped")
        else:
            await ctx.send("Im not playing anything")

def setup(client):
    client.add_cog(Music(client))