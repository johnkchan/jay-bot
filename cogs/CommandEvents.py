import discord
from discord.ext import commands

commands_tally = {}


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_command_completion(self, ctx):
    #     print(f"{ctx.command.name} was invoked successfully.")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None and ctx.command.name not in ["stats", "help"]:
            if ctx.command.name not in commands_tally:
                commands_tally[ctx.command.name] = 0
            commands_tally[ctx.command.name] += 1

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # if isinstance(error, commands.MissingRequiredArgument):
        #     await ctx.send('Please pass in all required arguments.')
        if ctx.message.content[:2] == "..":
            return

        if isinstance(error, commands.CommandNotFound):
            return await ctx.send("Invalid Command")

    @commands.command(name="stats")
    async def stats(self, ctx):
        if not commands_tally:
            return await ctx.send("No stats available yet")

        description = []
        for key, value in sorted(commands_tally.items(), key=lambda val: val[1], reverse=True):
            description.append(f"\n{key} - {value}")

        embed = discord.Embed(
            title="Jay Bot stats",
            description=''.join(description)
        )

        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandEvents(bot))
