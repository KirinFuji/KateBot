from discord.ext import commands


class MainCog(commands.Cog):
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.logging.log("MainCog", "Initialized", verbose=True, force=True)

    @commands.command(name="test2", pass_context=True)
    # @commands.has_role("Mod")
    async def test2(self, ctx):
        self.KateBot.logging.log("MainCog", "Initialized", verbose=True, force=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)


def setup(KateBot):
    KateBot.add_cog(MainCog(KateBot))
