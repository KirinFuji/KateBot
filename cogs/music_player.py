# Written by github.com/KirinFuji

#
#     .-.                 .-.
#    (_) )  .'-     /    (_) )-.            /
#       /  /.-. ---/---.-.  / __)  .-._.---/---
#     _/_.'(  |   /  ./.-'_/    `.(   )   /
#  .  /   \ `-'-'/   (__.'/'      )`-'   /
# (_.'     `-'         (_/  `----'

"""
MIT License

Copyright (c) 2021 KirinFuji@users.noreply.github.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from asyncio import run_coroutine_threadsafe
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from os import listdir, path
from os.path import isfile, join
from random import randint
# noinspection PyUnresolvedReferences
from KateLib import load_json_file, Log, safe_cast  # IDE Error: main.py is being run from a level lower
# noinspection PyUnresolvedReferences
from KateLib import RandomSymbols as Rs


class Queue:
    """Music Player Queue"""

    def __init__(self, KateBot):
        config = load_json_file('config/music_player.json')
        self.KateBot = KateBot
        self.music_home = config['music_location']
        self.ffmpeg = config['ffmpeg_location']
        Log.log("Queue",
                f'\n    - ffmpeg_location: {self.ffmpeg}\n    - music_location: {self.music_home}',
                Log.Type.debug)
        self.songList = []
        self.currentSong = None
        self.isPlaying = False
        self.source = None
        Log.log("Queue", "Initialized", Log.Type.debug)

    def enqueue(self, song):
        """!enqueue adds a single song to the queue"""
        self.songList.append(song)

    def next_track(self, voice_client):
        """Skips current song and plays next in queue"""
        if voice_client.is_playing():
            voice_client.stop()
            self.isPlaying = False

    def stop(self, voice_client):
        """Stops playback and empties queue"""
        if voice_client.is_playing():
            self.songList = []
            self.isPlaying = False
            voice_client.stop()
            # await self.KateBot.set_idle()  # Removed: Bot will be multi-server

    async def play(self, voice_client, song=None):
        """Main function for music player and queue"""
        if song is not None and song not in self.songList:
            Log.log("MusicPlayer", f"Queued Song: {song}", Log.Type.verbose)
            self.enqueue(song)
        if not self.isPlaying:
            if len(self.songList) > 0:
                self.currentSong = self.songList[0]
                self.songList.pop(0)
                full_path = f'{self.music_home}\\{self.currentSong}'
                if path.isfile(full_path):
                    Log.log("MusicPlayer", f"Playing Song: {self.currentSong}", None)
                    self.source = PCMVolumeTransformer(FFmpegPCMAudio(full_path, executable=self.ffmpeg), 0.5)
                    voice_client.play(self.source, after=lambda x: self.play_next(voice_client))
                    self.isPlaying = True
                    # await self.KateBot.set_listening(self.currentSong)  # Removed: Bot will be multi-server
                else:
                    Log.log("MusicPlayer", f"Music file not found!: \n {full_path}",
                            Log.Type.error)
                    raise FileNotFoundError
            else:
                # await self.KateBot.set_idle()  # Removed: Bot will be multi-server
                Log.log("MusicPlayer", "Queue is empty!", None)

    def change_volume(self, volume):
        """Sets the queues voice source volume"""
        if isinstance(self.source, PCMVolumeTransformer):
            if volume and 0 < volume <= 1.0:
                Log.log('MusicPlayer', f'Changing Volume to {volume}', Log.Type.verbose)
                self.source.volume = volume
            else:
                Log.log('MusicPlayer', f'Volume {volume}, out of range 0-1.0', Log.Type.error)

    def dequeue(self, song):
        """Remove single song from the queue"""
        if song in self.songList:
            self.songList.remove(song)
            Log.log("MusicPlayer", f"Removed: {song} from queue.", Log.Type.verbose)
        Log.log("MusicPlayer", f"{song} not in queue.", Log.Type.warning)

    def play_next(self, voice_client):
        """Workaround for calling async method from lambda"""
        Log.log("MusicPlayer", f"Song Finished: {self.currentSong}", Log.Type.verbose)
        self.isPlaying = False
        # Workaround to call asynchronous method from lambda
        run_coroutine_threadsafe(self.play(voice_client), self.KateBot.loop)

    async def play_playlist(self, voice_client, playlist):
        """Replace queue with a new playlist"""
        if len(playlist) > 0:
            self.songList = playlist
            await self.play(voice_client)

    def random_song_list(self, count):
        """generates a queue of <count> random songs"""
        Log.log("MusicPlayer", f"Generating Queue of {count} random songs!", Log.Type.verbose)
        only_files = [f for f in listdir(self.music_home) if isfile(join(self.music_home, f)) and f.endswith(".mp3")]
        song_list = []
        for i in range(count):
            song_list.append(only_files[randint(0, len(only_files))])
        return song_list


class MusicPlayer(commands.Cog):
    """MusicPlayer Cog"""

    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.Queues = {}
        self.enabled = True
        self.loaded = False
        Log.log("MusicPlayer", "Initialized", Log.Type.debug)

    @staticmethod
    def dump_voice_client(vc):
        """Dump voice client info"""
        if Log.debug:
            Log.log("MusicPlayer", f"Voice Client: {vc}\n    - session_id: {vc.session_id}"
                                   f"\n    - token: {vc.token}\n    - channel: {vc.channel}"
                                   f"\n    - loop: {vc.loop}\n    - guild: {vc.guild}"
                                   f"\n    - user: {vc.user}", Log.Type.debug)

    def get_guild_voice_client(self, ctx):
        """Get VoiceClient based on guild command was ran in"""
        voice_client = list(filter(lambda c: (c.guild == ctx.guild), self.KateBot.voice_clients))
        if voice_client:
            return voice_client[0]
        else:
            Log.log("MusicPlayer", "Voice Client not found!", Log.Type.error)
            return None

    @commands.Cog.listener()
    async def on_ready(self):
        """Register event loop"""
        if not self.loaded:
            self.loaded = True
            Log.log("MusicPlayer", "Loaded", Log.Type.verbose)

    @commands.command(name="join")
    @commands.guild_only()
    async def join_voice(self, ctx, *args):
        """!Join [channel_id] - Joins a discord voice channel"""
        Log.log("MusicPlayer", f"Joining Channel: {args[0]}", Log.Type.verbose)
        channel = self.KateBot.get_channel(int(args[0]))
        await channel.connect(timeout=60.0, reconnect=True)
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            self.dump_voice_client(voice_client)
            self.Queues[ctx.guild] = Queue(self.KateBot)

    @commands.command(name="leave")
    @commands.guild_only()
    async def leave_voice(self, ctx):
        """Leaves all connected voice channels"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            await voice_client.disconnect()
        self.Queues[ctx.guild] = None

    @commands.command(name="play")
    @commands.guild_only()
    async def play_music(self, ctx, *args):
        """!play <filename> plays an mp3 from disk"""
        if len(args) > 0:
            mp3 = args[0]
            if len(self.KateBot.voice_clients) > 0:
                voice_client = self.get_guild_voice_client(ctx)
                if voice_client:
                    await self.Queues[ctx.guild].play(voice_client, song=mp3)

    @commands.command(name='random_music')
    @commands.guild_only()
    async def random_music(self, ctx, *args):
        """Generates a queue of 5 random songs"""
        if len(self.KateBot.voice_clients) > 0:
            count = 5
            if len(args) > 0:
                count = safe_cast(args[0], int)
                if count is None:
                    await ctx.channel.send("Argument must be a number!")
            voice_client = self.get_guild_voice_client(ctx)
            if voice_client:
                await self.Queues[ctx.guild].play_playlist(voice_client, self.Queues[ctx.guild].random_song_list(count))

    @commands.command(name='stop')
    @commands.guild_only()
    async def stop_music(self, ctx):
        """Stops playback and empties queue"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            self.Queues[ctx.guild].stop(voice_client)

    @commands.command(name='skip')
    @commands.guild_only()
    async def next_music(self, ctx):
        """Skips current song and plays next in queue"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            self.Queues[ctx.guild].next_track(voice_client)

    @commands.command(name='pause')
    @commands.guild_only()
    async def pause_music(self, ctx):
        """Pauses music playback"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            voice_client.pause()

    @commands.command(name='resume')
    @commands.guild_only()
    async def resume_music(self, ctx):
        """Resumes music playback"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            voice_client.resume()

    @commands.command(name='volume')
    @commands.guild_only()
    async def change_volume(self, ctx, *args):
        """!volume [0-1.0] change volume 0-100% default: 50%"""
        #  value = int(args[0]) if args[0].isdecimal() else None
        value = safe_cast(args[0], float)
        if value:
            self.Queues[ctx.guild].change_volume(value)

    @commands.command(name='queue')
    @commands.guild_only()
    async def queue_cmd(self, ctx, *args):
        """!queue [command], [*args] - (length, *jump, *song)
           Provides sub commands for inspecting and managing queue"""
        if len(self.KateBot.voice_clients) > 0:
            if len(self.Queues[ctx.guild].songList) > 0:
                if len(args) > 0:
                    if 'song' == args[0]:
                        song_n = safe_cast(args[1], int)
                        if song_n:
                            await ctx.channel.send(f'Song: #{args[1]}, [ {self.Queues[ctx.guild].songList[song_n]} ]')
                    if 'length' == args[0]:
                        await ctx.channel.send(f'Currently {len(self.Queues[ctx.guild].songList)}')
                    if 'jump' == args[0]:
                        count = safe_cast(args[1], int)
                        if count:
                            for i in range(0, count):
                                self.Queues[ctx.guild].songList.pop(0)
                            await self.next_music(ctx)

    @commands.command(name='current', aliases=['playing'])
    @commands.guild_only()
    async def current_song(self, ctx):
        """Informs user of currently playing track"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            if voice_client.is_playing():
                track = self.Queues[ctx.guild].currentSong
                await ctx.channel.send(f"Currently Playing: [ {track.replace('.mp3', '')} ]! {Rs.random_heart()}")

    @commands.command(name='next_song', aliases=['next'])
    @commands.guild_only()
    async def next_song(self, ctx):
        """Informs user of currently playing track"""
        voice_client = self.get_guild_voice_client(ctx)
        if voice_client:
            if voice_client.is_playing():
                if len(self.Queues[ctx.guild].songList) > 1:
                    track = self.Queues[ctx.guild].songList[1]
                    await ctx.channel.send(f"Next up: [ {track.replace('.mp3', '')} ]! {Rs.random_heart()}")


def setup(KateBot):
    """Add cog to bot"""
    KateBot.add_cog(MusicPlayer(KateBot))
