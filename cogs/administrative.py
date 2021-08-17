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

from discord.ext import commands


class Administration(commands.Cog):
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.logging.log("Cog.Administration", "Initialized", verbose=True, force=True)

    @commands.command(name="shutdown", aliases=["quit", "logout"])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        try:
            await self.KateBot.close()
        except RuntimeError as err:
            self.KateBot.logging.log("Discord", f"{err}")
        self.KateBot.logging.log("Discord", "Logging Out!")

    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart(self, ctx):
        try:
            await self.KateBot.close()
        except RuntimeError as err:
            self.KateBot.logging.log("Discord", f"{err}")
        self.KateBot.logging.log("Discord", "Logging Out!")


def setup(KateBot):
    KateBot.add_cog(Administration(KateBot))
