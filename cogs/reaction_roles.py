from discord.ext import commands


class ReactionRoles(commands.Cog):
    """
    Reaction Roles
    This cog contains the code for parsing reactions.json and acting on incoming reactions.
    """
    def __init__(self, KateBot):
        self.KateBot = KateBot
        self.KateBot.logging.log("ReactionRoles", "Initialized", verbose=True, force=True)
        self.enabled = True

    @commands.command(name="disable_rr")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        """Disable Reaction Roles"""
        self.enabled = False
        self.KateBot.logging.log("ReactionRoles", "Disabled", verbose=True, force=True)

    @commands.command(name="enable__rr")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx):
        """Enable Reaction Roles"""
        self.enabled = True
        self.KateBot.logging.log("ReactionRoles", "Enabled", verbose=True, force=True)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     print(message.content)


def setup(KateBot):
    KateBot.add_cog(ReactionRoles(KateBot))
