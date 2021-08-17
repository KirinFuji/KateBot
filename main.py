import platform
import discord
from discord.utils import get
from discord.ext import commands
from _logging import Logging
from music_player import Queue
from KateLib import load_json_file, RandomSymbols
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
RS = RandomSymbols()


# Windows Development Fix
# https://github.com/aio-libs/aiohttp/issues/4324
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


class KateBot(commands.Bot):
    def __init__(self, Logger):
        intent = discord.Intents.default()
        config = load_json_file('config/discord.json')
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.logging.log("Discord", f"{error}\n"
                                    f" Author: [{ctx.author}]\n"
                                    f" Channel: [{ctx.channel}]", error=True)

    def add_commands(self):
        @self.command(name="shutdown", aliases=["quit", "logout"])
        @commands.has_permissions(administrator=True)
        async def close(ctx):
            try:
                await self.close()
            except RuntimeError as err:
                self.logging.log("Discord", f"{err}")
            self.logging.log("Discord", "Logging Out!")


if __name__ == '__main__':
    Log = Logging()
    Log.debug = True
    Log.bot = True
    Log.verbose = True
    Log.music_player = True
    Log.load()
    KBot = KateBot(Log)
    KBot.load_extension("cogs.reddit")
    #KBot.load_extension("cogs.template")
    KBot.run(KBot.token)



