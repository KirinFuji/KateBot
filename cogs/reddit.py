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
# noinspection PyUnresolvedReferences
from KateLib import load_json_file  # IDE Error: main.py is being run from a level lower
from discord.ext import commands
import asyncpraw as async_praw
from discord import Embed

class RedditCog(commands.Cog):
    """AsyncPraw Reddit Cog"""
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.log("Cog.Reddit", "Initialized", self.KateBot.Log.Type.verbose)
        config = load_json_file('config/reddit.json', KateBot.Log)
        self.meme_stream = config['meme_stream']
        self.meme_stream_channel = config['meme_stream_channel']
        self.enabled = True
        self.reddit = async_praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
            username=config['username'],
            password=config['password'])
        self.subs = config['monitored_subs']

    async def login_test(self):
        """Checks Reddit token validity and permissions"""
        reddit_user = await self.reddit.user.me()
        self.KateBot.log("Reddit", f"Logged in as {reddit_user.name} ReadOnly: {self.reddit.read_only}", None)

    @commands.Cog.listener()
    async def on_ready(self):
        """OnReady (Runs after discord login)"""
        await self.login_test()
        if self.meme_stream:
            self.register_streams()

    async def register_stream(self, _sub):
        """Creates an event loop submission stream"""
        subreddit = await self.reddit.subreddit(_sub)
        channel = self.KateBot.get_channel(self.meme_stream_channel)
        async for submission in subreddit.stream.submissions(skip_existing=True):
            try:
                title = submission.title[:255]  # embed.title: Must be 256 or fewer in length
                meme = Embed(title=title, url=f'https://www.reddit.com{submission.permalink}')
                meme.set_image(url=submission.url)
                self.KateBot.log('Reddit', f'({subreddit.display_name}) MemeStream: {meme.url}', None)
                new_msg = await channel.send(content=None, embed=meme)
                reactions = ['👍', '👎']
                for emoji in reactions:
                    await new_msg.add_reaction(emoji)
                # await asyncio.sleep(10)
            except Exception as e:
                print(f'Exception in register_stream: {e}')

    def register_streams(self):
        """Loop that spawns an event loop task for each subreddit."""
        for sub in self.subs:
            self.KateBot.log('Reddit', f'Registering MemeStream (/r/{sub})', None)
            self.KateBot.tasks.append(self.KateBot.loop.create_task(self.register_stream(sub)))
        self.KateBot.log('Reddit', 'All submission streams registered! ♥', self.KateBot.Log.Type.verbose)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Ignore Self
        if payload.user_id == self.KateBot.user.id:
            return
        # Logging
        self.KateBot.log('Discord', f'Detected {payload.emoji} add from {payload.member} '
                                    f'@g {payload.guild_id} @c {payload.channel_id} @m {payload.message_id}',
                                    self.KateBot.Log.Type.debug)
        # Reddit Up/Down-Vote
        if payload.channel_id == self.meme_stream_channel:
            channel = self.KateBot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.author.id == self.KateBot.user.id:
                if payload.user_id in self.KateBot.owner_ids:
                    reddit_post = message.embeds[0].url
                    self.KateBot.log("Discord", f'User: {payload.member} reacted to {reddit_post} with {payload.emoji}',
                                     self.KateBot.Log.Type.verbose)
                    submission = await self.reddit.submission(url=reddit_post)
                    if payload.emoji.name == '👍':
                        await submission.upvote()
                        self.KateBot.log("Reddit", f'Up-Vote: {reddit_post}', None)
                    elif payload.emoji.name == '👎':
                        await submission.downvote()
                        self.KateBot.log("Reddit", f'Down-Vote: {reddit_post}', None)


def setup(KateBot):
    """Create Cog object and add it to KateBot"""
    reddit_instance = RedditCog(KateBot)
    KateBot.reddit = reddit_instance.reddit
    KateBot.add_cog(reddit_instance)



