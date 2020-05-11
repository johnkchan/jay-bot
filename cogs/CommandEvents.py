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
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # if isinstance(error, commands.MissingRequiredArgument):
        #     await ctx.send('Please pass in all required arguments.')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid Command")

    @commands.command(name="stats")
    async def stats(self, ctx):
        if commands_tally:
            description = []
            for key, value in sorted(commands_tally.items(), key=lambda kv: kv[1], reverse=True):
                description.append(f"\n{key} - {value}")

            embed = discord.Embed(
                title="jay_bot stats",
                description=''.join(description)
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send("No stats available yet")


def setup(bot):
    bot.add_cog(CommandEvents(bot))
