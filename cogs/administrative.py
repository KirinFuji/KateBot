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
import pprint

import discord.ext.commands
from discord.ext import commands
from discord import Color, Embed
from KateLib import RandomSymbols, Log


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
        self.enabled = True
        self.loaded = False
        Log.log("Administration", "Initialized", Log.Type.debug)

    @commands.Cog.listener()
    async def on_ready(self):
        """Register event loop"""
        if not self.loaded:
            self.loaded = True
            Log.log("Administration", "Loaded", Log.Type.verbose)

    # Shutdown Command
    @commands.command(name="shutdown", aliases=["quit", "logout"])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx: discord.ext.commands.Context):
        """Shuts down KateBot! (Admin Only)"""
        try:
            await ctx.channel.send(f'Bye! {RandomSymbols.random_heart()}')
            await self.KateBot.close()
        except RuntimeError as err:
            Log.log("Discord", f"{err}", Log.Type.error)
        Log.log("Discord", "Logging Out!", None)

    # Restart Command
    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart(self, _ctx: discord.ext.commands.Context):
        """Restarts KateBot (Admin Only)"""
        try:
            await self.KateBot.close()
        except RuntimeError as err:
            Log.log("Discord", f"{err}", Log.Type.error)
        Log.log("Discord", "Logging Out!", None)

    # Cleanup Command
    @commands.command(name='cleanup', aliases=['clean', 'scrub'])
    @commands.guild_only()
    @commands.is_owner()
    async def cleanup(self, ctx: discord.ext.commands.Context, *args):
        """!Cleanup [all|<username>] Starts deleting messages in the channel the command is run, up to 200."""
        messages = await ctx.channel.history(limit=200).flatten()
        for m in messages:
            if 'all' in args:
                Log.log('Discord', f'Deleting: {m.author.name}: {m.content}', Log.Type.verbose)
                await asyncio.sleep(0.2)
                await m.delete()
            elif m.author.name in args:
                Log.log('Discord', f'Deleting: {m.author.name}: {m.content}', Log.Type.verbose)
                await asyncio.sleep(0.2)
                await m.delete()

    # Bulk delete
    @commands.command(name='bulk_delete')
    @commands.guild_only()
    @commands.is_owner()
    async def bulk_delete(self, ctx: discord.ext.commands.Context):
        """Bulk delete 100 messages at a time (Max age of 14 days for bulk deletable messages)"""
        messages = await ctx.channel.history(limit=100).flatten()
        await ctx.channel.delete_messages(messages)

    @commands.command(name='debug')
    @commands.guild_only()
    @commands.is_owner()
    async def debug_test(self, ctx: discord.ext.commands.Context):
        """Debug command to dump context"""
        pprint.pprint(vars(ctx))
        await ctx.message.delete()

    @commands.command(name='msgdebug')
    @commands.guild_only()
    @commands.is_owner()
    async def msg_debug_test(self, ctx: discord.ext.commands.Context, *args):
        """Debug command to dump context"""
        message = await ctx.fetch_message(args[0])
        pprint.pprint(dir(message))
        print(f"Type:{message.type}")
        print(f"Embeds:{message.embeds}")
        pprint.pprint(message.embeds[0].to_dict())
        await ctx.message.delete()

    # Status Command
    @commands.command(name="status")
    @commands.guild_only()
    async def status(self, ctx: discord.ext.commands.Context):
        """Is the bot still alive command."""
        await ctx.channel.send(f'I\'m still here, {ctx.author.name}! {RandomSymbols.random_heart()}')


def setup(KateBot):
    """Add cog to bot"""
    cog = Administration(KateBot)
    KateBot.help_command = CustomHelp()
    KateBot.add_cog(cog)
