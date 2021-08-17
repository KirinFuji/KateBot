# Written by github.com/KirinFuji

# NOTICE #
# PyNaCl library needed in order to use MusicPlayer

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
from KateLib import load_json_file  # IDE Error: main.py is being run from a level lower

class Queue:
    def __init__(self, KateBot):
        config = load_json_file('config/music_player.json', KateBot.Log)
        self.KateBot = KateBot
        self.songList = []
        self.currentSong = None
        self.isPlaying = False
        self.music_home = config['music_location']
        self.ffmpeg = config['ffmpeg_location']
        self.paused = False
        self.KateBot.log("Cog.MusicPlayer.Queue", "Initialized", self.KateBot.Log.Type.verbose)
        self.KateBot.log("Cog.MusicPlayer.Queue",
                         f'\n    - ffmpeg_location: {self.ffmpeg}\n    - music_location: {self.music_home}',
                         self.KateBot.Log.Type.debug)

    def enqueue(self, song):
        self.songList.append(song)

    def pause(self, client):
        if client.is_playing():
            client.pause()
            self.paused = True

    def next(self, client):
        if client.is_playing():
            client.stop()
            self.isPlaying = False

    async def stop(self, client):
        if client.is_playing():
            self.songList = []
            self.isPlaying = False
            client.stop()
            await self.KateBot.set_idle()

    def resume(self, client):
        client.resume()
        self.paused = False

    async def play(self, client, song=None):
        """Main function for music player and queue"""
        if song is not None and song not in self.songList:
            self.KateBot.log("MusicPlayer", f"Queued Song: {song}", self.KateBot.Log.Type.verbose)
            self.enqueue(song)
        if not self.isPlaying:
            if len(self.songList) > 0:
                self.currentSong = self.songList[0]
                self.songList.pop(0)
                full_path = f'{self.music_home}\\{self.currentSong}'
                if path.isfile(full_path):
                    self.KateBot.log("MusicPlayer", f"Playing Song: {self.currentSong}", None)
                    audio_source = FFmpegPCMAudio(full_path, executable=self.ffmpeg)
                    client.play(PCMVolumeTransformer(audio_source, 0.8),
                                after=lambda x: self.play_next(client))
                    self.isPlaying = True
                    await self.KateBot.set_listening(self.currentSong)
                else:
                    self.KateBot.log("MusicPlayer", f"Music file not found!: \n {full_path}",
                                     self.KateBot.Log.Type.error)
                    raise FileNotFoundError
            else:
                await self.KateBot.set_idle()
                self.KateBot.log("MusicPlayer", "Queue is empty!", self.KateBot.Log.Type.warning)

    def dequeue(self, song):
        if song in self.songList:
            self.songList.remove(song)
            self.KateBot.log("MusicPlayer", f"Removed: {song} from queue.", self.KateBot.Log.Type.verbose)
        self.KateBot.log("MusicPlayer", f"{song} not in queue.", self.KateBot.Log.Type.warning)

    def play_next(self, client):
        """Workaround for calling async method from lambda"""
        self.KateBot.log("MusicPlayer", f"Song Finished: {self.currentSong}", self.KateBot.Log.Type.verbose)
        self.isPlaying = False
        # Workaround to call asynchronous method from lambda
        run_coroutine_threadsafe(self.play(client), self.KateBot.loop)

    async def play_playlist(self, client, playlist):
        if len(playlist) > 0:
            self.songList = playlist
            await self.play(client)

    def random_song_list(self, count):
        self.KateBot.log("MusicPlayer", f"Generating Queue of {count} random songs!", self.KateBot.Log.Type.verbose)
        only_files = [f for f in listdir(self.music_home) if isfile(join(self.music_home, f)) and f.endswith(".mp3")]
        song_list = []
        for i in range(count):
            song_list.append(only_files[randint(0, len(only_files))])
        return song_list


class MusicPlayer(commands.Cog):
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.queue = Queue(self.KateBot)
        self.KateBot.log("Cog.MusicPlayer", "Initialized", self.KateBot.Log.Type.verbose)
        self.enabled = True

    # Voice Channel

    @commands.command(name="join")
    @commands.guild_only()
    async def join_voice(self, ctx, *args):
        """!Join [channel_id] - Joins a discord voice channel"""
        self.KateBot.log("MusicPlayer", f"Joining Channel: {args[0]}", self.KateBot.Log.Type.verbose)
        channel = self.KateBot.get_channel(int(args[0]))
        await channel.connect(timeout=60.0, reconnect=True)
        vc = self.KateBot.voice_clients[0]
        self.KateBot.log("MusicPlayer", f"Voice Client: {vc}\n    - session_id: {vc.session_id}"
                                        f"\n    - token: {vc.token}\n    - channel: {vc.channel}"
                                        f"\n    - loop: {vc.loop}\n    - guild: {vc.guild}"
                                        f"\n    - user: {vc.user}", self.KateBot.Log.Type.debug)

    @commands.command(name="leave")
    @commands.guild_only()
    async def leave_voice(self, ctx, *args):
        for client in self.KateBot.voice_clients:
            await client.disconnect()

    @commands.command(name="play", pass_context=False)
    @commands.guild_only()
    async def play_music(self, ctx, *args):
        if len(args) > 0:
            mp3 = args[0]
            if len(self.KateBot.voice_clients) > 0:
                await self.queue.play(self.KateBot.voice_clients[0], song=mp3)

    @commands.command(name='random_music', pass_context=False)
    @commands.guild_only()
    async def random_music(self, ctx):
        if len(self.KateBot.voice_clients) > 0:
            await self.queue.play_playlist(self.KateBot.voice_clients[0], self.queue.random_song_list(5))

    @commands.command(name='stop', pass_context=False)
    @commands.guild_only()
    async def stop_music(self, ctx):
        if len(self.KateBot.voice_clients) > 0:
            self.queue.stop(self.KateBot.voice_clients[0])

    @commands.command(name='next', pass_context=False)
    @commands.guild_only()
    async def next_music(self, ctx):
        if len(self.KateBot.voice_clients) > 0:
            self.queue.next(self.KateBot.voice_clients[0])

    @commands.command(name='pause', pass_context=False)
    @commands.guild_only()
    async def pause_music(self, ctx):
        if len(self.KateBot.voice_clients) > 0:
            self.queue.pause(self.KateBot.voice_clients[0])

    @commands.command(name='resume', pass_context=False)
    @commands.guild_only()
    async def resume_music(self, ctx):
        if len(self.KateBot.voice_clients) > 0:
            self.queue.resume(self.KateBot.voice_clients[0])


def setup(KateBot):
    KateBot.add_cog(MusicPlayer(KateBot))
