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
from discord import Embed
from discord.ext import commands
from KateLib import load_json_file, RandomSymbols, Log
from re import search
from aiohttp import ClientSession

class Misc(commands.Cog):
    """Basic cog template"""
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.loaded = False
        Log.log("Misc", "Initialized", Log.Type.debug)

    @commands.command(name="yetee", aliases=["daily_tees"])
    async def test2(self, ctx):
        """Sample cog command"""
        async with ClientSession() as session:
            async with session.get('https://theyetee.com/collections/daily-tees') as resp:
                text = await resp.text()
                lines = text.splitlines()
                links = []
                line_n = 0
                for line in lines:
                    if 'swiper-main' in line:
                        #  print(f'[{line_n}]{line}')
                        #  print(f'[{line_n}]{lines[line_n + 1]}')
                        data = lines[line_n + 1]
                        match = search(r'href=[\'"]?([^\'" >]+)', data)

                        if match:
                            url = match.group(1)
                            link = url[2:]
                            links.append(link)
                    line_n += 1
        for link in links:
            embed = Embed(title="Today's Tee", url='https://theyetee.com/collections/daily-tees')
            embed.set_image(url='https://'+link)
            await ctx.channel.send(content=None, embed=embed)


def setup(KateBot):
    """Adds the cog to the bot"""
    KateBot.add_cog(Misc(KateBot))
