import discord
from discord.ext import commands


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def helpcommand(self, ctx):
        embed = discord.Embed(
            title="Jay Bot commands",
            description="The prefix of the bot is `.`"
        )
        embed.add_field(
            name='API', value="`ah` `dank` `dh` `dictionary` `funfact` `gif` `joke` `movie` `ph` `translate` `urbandict` `yelp` `weather`", inline=False)
        embed.add_field(
            name='General', value="`ping` `poll` `stats`", inline=False)
        embed.add_field(
            name='Misc', value="`clear` `tts`", inline=False)
        embed.add_field(
            name='Random', value="`8ball` `coinflip` `madgab` `percent` `roll` `teams`", inline=False)

        embed.set_footer(text="for more information try .help (command)")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
