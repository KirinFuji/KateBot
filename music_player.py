# Written by github.com/KirinFuji

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

from discord import FFmpegPCMAudio, PCMVolumeTransformer
from os import listdir, path
from os.path import isfile, join
from random import randint
from KateLib import load_json_file


class Queue:
    def __init__(self, Logger):
        config = load_json_file('config/music_player.json')
        self.songList = []
        self.currentSong = None
        self.isPlaying = False
        self.music_home = config['music_location']
        self.ffmpeg = config['ffmpeg_location']
        self.paused = False
        self.logging = Logger
        self.logging.log("MusicBot", "Initialized", verbose=True)

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

    def stop(self, client):
        if client.is_playing():
            self.songList = []
            self.isPlaying = False
            client.stop()

    def resume(self, client):
        client.resume()
        self.paused = False

    def play(self, client, song=None):
        if song is not None and song not in self.songList:
            self.logging.log("MusicBot", f"Queued Song: {song}", verbose=True)
            self.enqueue(song)
        if not self.isPlaying:
            if len(self.songList) > 0:
                self.currentSong = self.songList[0]
                self.songList.pop(0)
                full_path = f'{self.music_home}\\{self.currentSong}'
                if path.isfile(full_path):
                    self.logging.log("MusicBot", f"Playing Song: {self.currentSong}")
                    audio_source = FFmpegPCMAudio(full_path, executable=self.ffmpeg)
                    client.play(PCMVolumeTransformer(audio_source, 0.8),
                                after=lambda x: self.play_next(client))
                    self.isPlaying = True
                else:
                    self.logging.log("MusicBot", f"Music file not found!: \n {full_path}", error=True)
                    raise FileNotFoundError
            else:
                self.logging.log("MusicBot", "Queue is empty!", warning=True)

    def dequeue(self, song):
        if song in self.songList:
            self.songList.remove(song)
            self.logging.log("MusicBot", f"Removed: {song} from queue.", verbose=True)
        self.logging.log("MusicBot", f"{song} not in queue.", warning=True)

    def play_next(self, client):
        self.logging.log("MusicBot", f"Song Finished: {self.currentSong}", verbose=True)
        self.isPlaying = False
        if len(self.songList) > 0:
            self.play(client)
        else:
            self.logging.log("MusicBot", f"Queue Finished!", verbose=True)
            self.isPlaying = False

    def play_playlist(self, client, playlist):
        if len(playlist) > 0:
            self.songList = playlist
            self.play(client)

    def random_song_list(self, count):
        self.logging.log("MusicBot", f"Generating Queue of {count} random songs!", verbose=True)
        only_files = [f for f in listdir(self.music_home) if isfile(join(self.music_home, f)) and f.endswith(".mp3")]
        song_list = []
        for i in range(count):
            song_list.append(only_files[randint(0, len(only_files))])
        return song_list
