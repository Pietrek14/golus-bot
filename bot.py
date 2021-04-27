import discord
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
NAME = os.getenv("NAME")
SONGS_DIRECTORY = os.getenv("SONGS_DIRECTORY")
FFMPEG_PATH = "G:/rurzne_zeczy/golu/bot_golusa/ffmpeg-20200831-4a11a6f-win64-static/bin/ffmpeg.exe"

SONGS = []
for song in os.scandir(SONGS_DIRECTORY):
    if song.is_file():
        SONGS.append(f"{SONGS_DIRECTORY}/{song.name}")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_voice_state_update(self, member, before, after):
        # Jesli sie dolaczyl
        if member.name == NAME and not after.channel is None and before.channel != after.channel:
            if not self.user in after.channel.members:
                voice_client = await after.channel.connect()
                def disconnect(err):
                    future = asyncio.run_coroutine_threadsafe(voice_client.disconnect(), client.loop)
                    try:
                        future.result()
                    except:
                        print("kurcze blaszka")
                voice_client.play(discord.FFmpegPCMAudio(source=random.choice(SONGS), executable=FFMPEG_PATH), after=disconnect)
        
        # Jesli sie rozlaczyl
        if member.name == NAME and not before.channel is None and after.channel != before.channel:
            if self.user in before.channel.members:
                await before.channel.guild.voice_client.disconnect()

client = MyClient()
client.run(TOKEN)