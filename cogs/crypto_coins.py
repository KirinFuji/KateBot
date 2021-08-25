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

# NOTICE: Web requests written for coinmarketcap.com with requests kept below daily max for free plan

from json import loads
from discord.ext import commands
from KateLib import load_json_file, safe_get, Log
import aiohttp
import asyncio


class CryptoCoins(commands.Cog):
    """CryptoCurrency cog (WIP)"""
    def __init__(self, KateBot):
        self.KateBot = KateBot
        config = load_json_file('config/crypto.json')
        self.token = config['token']
        self.crypto_feed = int(config['crypto_feed'])
        self.coins = config['coins']
        self.price_alerts = config['price_alerts']
        self.default_headers = {"X-CMC_PRO_API_KEY": self.token, "Accept": "application/json"}
        self.loaded = False
        Log.log("CryptoCoins", "Initialized", Log.Type.debug)

    async def periodic_coin_check(self):
        """Periodically fetches current crypto price and adds to crypto-feed channel"""
        channel = self.KateBot.get_channel(self.crypto_feed)
        while self.price_alerts:
            text = ''
            for coin in self.coins:
                data = await self.fetch_coin(coin)
                price = '${:,.2f}\n'.format(data['data'][str(coin)]['quote']['USD']['price'])
                text += price
            await channel.send(text.rstrip())
            await asyncio.sleep(300)

    def register_alerts(self):
        """Registers periodic_coin_check event loop"""
        print("Adding Crypto Task")
        task = self.KateBot.loop.create_task(self.periodic_coin_check())
        task.set_name("CryptoCoins_Checker")
        self.KateBot.tasks.append(task)

    @commands.Cog.listener()
    async def on_ready(self):
        """Register event loop"""
        if not self.loaded:
            self.loaded = True
            valid = await self.is_token_valid()
            Log.log("CryptoCoins", f"API Key: {valid}", None)
            if valid:
                Log.log("CryptoCoins", "Loaded", Log.Type.verbose)
                if self.price_alerts:
                    self.register_alerts()
            else:
                Log.log("CryptoCoins", "Failed to validate API token!", Log.Type.error)

    async def fetch_coin(self, coinID):
        """CoinMarketCap API -- Single Currency Query by ID"""
        async with aiohttp.ClientSession(headers=self.default_headers) as session:
            parameters = {'id': str(coinID), 'convert': 'USD'}
            async with session.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
                                   params=parameters) as resp:
                return loads(await resp.text())

    async def is_token_valid(self):
        """CoinMarketCap API -- Returns API key details and usage stats"""
        async with aiohttp.ClientSession(headers=self.default_headers) as session:
            async with session.get('https://pro-api.coinmarketcap.com/v1/key/info') as resp:
                data = loads(await resp.text())
                result = safe_get(data, 'status', 'error_code')
                if result == 0:
                    remaining = safe_get(data, 'data', 'usage', 'current_day', 'credits_left')
                    if remaining is not None and remaining > 0:
                        return True
                return False

    @commands.command(name="price")
    @commands.guild_only()
    async def price(self, ctx, *args):
        """Fetch Crypto Price (WIP)"""
        if len(args) > 0:
            response = await self.fetch_coin(args[0])
            raw = response['data'][str(args[0])]['quote']['USD']['price']
            text = '${:,.2f}'.format(raw)
            await ctx.channel.send(text)
        else:
            await ctx.channel.send("Missing currency id!")


def setup(KateBot):
    """Add cog to bot"""
    KateBot.add_cog(CryptoCoins(KateBot))
