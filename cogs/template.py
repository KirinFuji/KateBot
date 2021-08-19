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

from discord.ext import commands
# noinspection PyUnresolvedReferences
from KateLib import load_json_file, RandomSymbols  # IDE Error: main.py is being run from a level lower


class TemplateCog(commands.Cog):
    """Basic cog template"""
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.loaded = False
        self.KateBot.log("TemplateCog", "Initialized", self.KateBot.Log.Type.debug)

    @commands.command(name="template_command", aliases=["test_command", "test_command2"])
    @commands.has_role("Basic Access")
    async def test2(self, ctx):
        """Sample cog command"""
        ctx.channel.send(f"Hai! :D {RandomSymbols.random_heart()}")
        self.KateBot.Log.log("TemplateCog", "TestCommand", verbose=True, force=True)

    @commands.Cog.listener()
    async def on_ready(self):
        """Register event loop"""
        if not self.loaded:
            self.loaded = True
            self.KateBot.log("TemplateCog", "Loaded", self.KateBot.Log.Type.verbose)


def setup(KateBot):
    """Adds the cog to the bot"""
    KateBot.add_cog(TemplateCog(KateBot))
