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
from discord.utils import get
# noinspection PyUnresolvedReferences
from KateLib import load_json_file  # IDE Error: main.py is being run from a level lower


class ReactionRoles(commands.Cog):
    """
    Reaction Roles
    This cog contains the code for parsing reactions.json and acting on incoming reactions.
    """
    def __init__(self, KateBot):
        self.reactions = load_json_file('config/reactions.json', KateBot.Log)
        self.KateBot = KateBot
        self.KateBot.log("Cog.ReactionRoles", "Initialized", KateBot.Log.Type.verbose)
        self.enabled = True

    async def reaction_role(self, payload, emoji, role_name, remove=False):
        """Primary Logic flow for adding/removing roles"""
        self.KateBot.log("ReactionRoles", f"\n  -Emoji: {payload.emoji.name} | {emoji}"
                                          f"\n  -Role: {role_name}"
                                          f"\n  -Remove: {remove}"
                                          f"\n  -Member: {payload.member}", self.KateBot.Log.Type.debug)
        if payload.emoji.name == emoji:

            role = get(payload.member.guild.roles, name=role_name)
            if role is not None:
                if role not in payload.member.roles:
                    await payload.member.add_roles(role)
                    self.KateBot.log("ReactionRoles", f"({role_name}) added to ({payload.member})", None)
                elif remove:
                    await payload.member.remove_roles(role)
                    self.KateBot.log("ReactionRoles", f"({role_name}) removed from ({payload.member})", None)
            else:
                self.KateBot.log("ReactionRoles", f"Role ({role_name}) not found in guild ({payload.member.guild})",
                                 self.KateBot.Log.Type.error)
                raise TypeError(f"({role_name}) not found in guild ({payload.member.guild})")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Reaction Roles"""
        # Reactions Loop (reactions.json)
        for reaction in self.reactions:
            if payload.message_id == reaction["message_id"]:
                await self.reaction_role(payload, reaction["emoji"], reaction["role_name"])

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.KateBot.user.id:
            return

        # Requires Members Intent
        guild = self.KateBot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        payload.member = member
        for reaction in self.reactions:
            if payload.message_id == reaction["message_id"]:
                await self.reaction_role(payload, reaction["emoji"], reaction["role_name"], remove=True)

    @commands.command(name="rr_disable")
    @commands.has_permissions(administrator=True)
    async def rr_disable(self, ctx):
        """Disable Reaction Roles"""
        self.enabled = False
        self.KateBot.log("ReactionRoles", "Disabled", None)

    @commands.command(name="rr_enable")
    @commands.has_permissions(administrator=True)
    async def rr_enable(self, ctx):
        """Enable Reaction Roles"""
        self.enabled = True
        self.KateBot.log("ReactionRoles", "Enabled", None)

    @commands.command(name="rr_reload")
    @commands.has_permissions(administrator=True)
    async def rr_reload(self, ctx):
        """Reload Reaction Roles Json"""
        self.reactions = load_json_file('config/reactions.json', self.KateBot.Log)
        self.KateBot.log("ReactionRoles", "Reloaded JSON!", None)
        await ctx.channel.send("[ReactionRoles]: Reloaded JSON!")

def setup(KateBot):
    #
    """Called by adding extension in main.py"""
    KateBot.add_cog(ReactionRoles(KateBot))

    """ Old Code from Before separation"""
    """    
    try:
        if KateBot.cogs['RedditCog']:
            KateBot.add_cog(ReactionRoles(KateBot))
    except KeyError as err:
        KateBot.log("Reddit", "RedditCog missing!", KateBot.Log.Type.error)
        raise ModuleNotFoundError("Reactions Module Requires RedditCog")
    """


