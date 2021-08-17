from discord.ext import commands


class RedditCog(commands.Cog):
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.logging.log("Reddit", "Initialized", verbose=True, force=True)


def setup(KateBot):
    KateBot.add_cog(RedditCog(KateBot))
