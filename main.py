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

import platform
import discord
from discord.utils import get
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from LogLib import Logging
from music_player import Queue
from KateLib import load_json_file, RandomSymbols
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport # IDE Error: This exists on windows.
RS = RandomSymbols()


# Windows Development Fix
# Big thanks to https://github.com/paaksing for this snippet!
# https://github.com/aio-libs/aiohttp/issues/4324
# http://www.apache.org/licenses/LICENSE-2.0
""" This code serves to fix a crash that specifically happens on windows due to the aiohttp 
library using a different underlying mechanism on windows. See issue 4324 for more information."""


def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


if platform.system() == 'Windows':
    # Silence the exception here.
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
# End Windows Development Fix


class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        channel = self.get_destination()
        embed = discord.Embed(color=discord.Color.blurple())
        for page in self.paginator.pages:
            embed.description += page
        await channel.send(embed=embed)

# Discord.py Bot Extension
class KateBot(commands.Bot):
    def __init__(self, Logger):

        config = load_json_file('config/discord.json')

        intent = discord.Intents.default()
        intent.members = config['members_intent']
        intent.typing = config['typing_intent']
        intent.presences = config['presences_intent']

        commands.Bot.__init__(self,
                              owner_ids=config['owner_ids'],
                              command_prefix=config['prefix'],
                              case_insensitive=config['case_insensitive'],
                              intents=intent)

        self.token = config['token']
        self.logging = Logger
        self.player = Queue(Logger=Logger)

        self.add_commands()
        self.logging.log('KateBot', "Initialized", verbose=True)

    @staticmethod
    async def reaction_role(payload, emoji, role_name, remove=False):
        if payload.emoji.name == emoji:
            role = get(payload.member.guild.roles, name=role_name)
            if role is not None:
                if role not in payload.member.roles:
                    await payload.member.add_roles(role)
                elif remove:
                    await payload.member.remove_roles(role)
            else:
                raise TypeError(f"Role ({role_name}) not found in guild ({payload.member.guild})")

    async def on_ready(self):
        self.logging.log('Discord', f'Logged in as {self.user}! {RS.random_heart()}')

    async def on_command_error(self, ctx, error):
        self.logging.log("Discord", f"{error}\n"
                                    f" Author: [{ctx.author}]\n"
                                    f" Channel: [{ctx.channel}]", error=True)

    # IDE Bug? Self should be purple.
    def add_commands(self):
        @self.command(name="shutdown", aliases=["quit", "logout"])
        @commands.has_permissions(administrator=True)
        async def shutdown(ctx):
            try:
                await self.close()
            except RuntimeError as err:
                self.logging.log("Discord", f"{err}")
            self.logging.log("Discord", "Logging Out!")

        @self.command(category="administrative", name="restart",
                      brief='Restart bot', description='Restarts the discord bot.')
        @commands.has_permissions(administrator=True)
        async def shutdown(ctx):
            try:
                await self.close()
            except RuntimeError as err:
                self.logging.log("Discord", f"{err}")
            self.logging.log("Discord", "Logging Out!")


if __name__ == '__main__':

    # SQL Alchemy Setup
    engine = create_engine(f"sqlite:///database.db")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Logging Setup
    Log = Logging()
    Log.debug = True
    Log.bot = True
    Log.verbose = True
    Log.music_player = True
    Log.load()

    # KateBot Setup
    KBot = KateBot(Log)
    KBot.load_extension("cogs.reddit")
    KBot.help_command = CustomHelp()
    KBot.load_extension("cogs.reaction_roles")
    # KBot.load_extension("cogs.template")

    # Entry Point
    KBot.run(KBot.token)



