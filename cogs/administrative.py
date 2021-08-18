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
import asyncio

from discord.ext import commands
from discord import Color, Embed
# noinspection PyUnresolvedReferences
from KateLib import RandomSymbols  # IDE Error: main.py is being run from a level lower


class CustomHelp(commands.MinimalHelpCommand):
    """Custom Discord Help Command"""

    async def send_pages(self):
        """Modified send_pages sends the information in an embed"""
        channel = self.get_destination()
        embed = Embed(color=Color.blurple(), description='')
        for page in self.paginator.pages:
            embed.description += page
        await channel.send(embed=embed)


class Administration(commands.Cog):
    """Administrative commands for running the bot."""
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.log("Cog.Administration", "Initialized", self.KateBot.Log.Type.verbose)
        self.enabled = True
        self.RS = RandomSymbols()

    @commands.command(name="shutdown", aliases=["quit", "logout"])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """Shuts down KateBot! (Admin Only)"""
        try:
            await ctx.channel.send(f'Bye! {self.RS.random_heart()}')
            await self.KateBot.close()
        except RuntimeError as err:
            self.KateBot.Log.log("Discord", f"{err}")
        self.KateBot.log("Discord", "Logging Out!", None)

    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart(self, _ctx):
        """Restarts KateBot (Admin Only)"""
        try:
            await self.KateBot.close()
        except RuntimeError as err:
            self.KateBot.Log.log("Discord", f"{err}")
        self.KateBot.log("Discord", "Logging Out!", None)

    # Cleanup Command
    @commands.command(name='cleanup', aliases=['clean', 'scrub'])
    @commands.guild_only()
    @commands.is_owner()
    async def cleanup(self, ctx, *args):
        """!Cleanup [all|<username>] Starts deleting messages in the channel the command is run, up to 200."""
        messages = await ctx.channel.history(limit=200).flatten()
        for m in messages:
            if 'all' in args:
                self.KateBot.log('Discord', f'Deleting: {m.author.name}: {m.content}', self.KateBot.Log.Type.verbose)
                await asyncio.sleep(1)
                await m.delete()
            elif m.author.name in args:
                self.KateBot.log('Discord', f'Deleting: {m.author.name}: {m.content}', self.KateBot.Log.Type.verbose)
                await asyncio.sleep(1)
                await m.delete()

    # Status Command
    @commands.command(name="status")
    @commands.guild_only()
    async def status(self, ctx):
        """Is the bot still alive command."""
        await ctx.channel.send(f'I\'m still here, {ctx.author.name}! {self.RS.random_heart()}')


def setup(KateBot):
    """Add cog to bot"""
    cog = Administration(KateBot)
    KateBot.help_command = CustomHelp()
    KateBot.add_cog(cog)
