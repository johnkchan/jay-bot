import discord
from discord.ext import commands, tasks


class AdminEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            return await channel.send(f"Hi <@!{member.id}>")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            return await channel.send(f"Good bye <@!{member.id}>")


def setup(bot):
    bot.add_cog(AdminEvents(bot))
