from discord.ext import commands


class ReactionRoles(commands.Cog):
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.logging.log("ReactionRoles", "Initialized", verbose=True, force=True)
        self.enabled = True

    @commands.command(name="disable", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        self.enabled = False
        self.KateBot.logging.log("ReactionRoles", "Disabled", verbose=True, force=True)

    @commands.command(name="enable", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        self.enabled = True
        self.KateBot.logging.log("ReactionRoles", "Enabled", verbose=True, force=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)


def setup(KateBot):
    KateBot.add_cog(ReactionRoles(KateBot))
