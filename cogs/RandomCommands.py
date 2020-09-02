from discord.ext import commands
import random
from madgab import prompts


class RandomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", description="Jay Bot flips a coin", aliases=["flip", "flipcoin"])
    async def coinflip(self, ctx):
        return await ctx.send(f"{random.choice(['heads', 'tails'])}")

    @commands.command(name="roll", description="Jay Bot rolls a dice")
    async def roll(self, ctx, amount=1):
        if amount == 1:
            return await ctx.send(f"🎲 You rolled a {random.randrange(1, 7)}")

        rolls = [random.randrange(1, 7) for _ in range(amount)]
        concatenation = ", ".join(map(str, rolls))
        return await ctx.send(f"🎲 You rolled {concatenation} = {sum(rolls)}.")

    @commands.command(name="percent", description="Jay Bot gives you a percent")
    async def percent(self, ctx, *, question=""):
        return await ctx.send(f"{random.randrange(0, 101)}%")

    @commands.command(name="8ball", description="Jay Bot answers your questions")
    async def _8ball(self, ctx, *, question):
        responses = ["As I see it, yes",
                     "Ask again later",
                     "Better not tell you now",
                     "Cannot predict now",
                     "Concentrate and ask again",
                     "Don't count on it",
                     "It is certain",
                     "It is decidedly so",
                     "Most likely",
                     "My reply is no",
                     "Outlook not so good",
                     "Outlook good",
                     "Reply hazy, try again",
                     "Signs point to yes",
                     "Very doubtful",
                     "Without a doubt",
                     "Yes",
                     "Yes - definitely",
                     "You may rely on it"]
        return await ctx.send(f"🎱 {random.choice(responses)}")

    @commands.command(name="teams", description="Jay Bot randomizes team members")
    async def teams(self, ctx, *, members):
        teams = [[], []]
        delimiter = ", "
        members = members.split(delimiter)

        i = 0
        while members:
            rand_int = random.randrange(0, len(members))
            member = members.pop(rand_int)
            teams[i].append(member)
            i += 1
            i %= 2

        return await ctx.send(f"Team A: {delimiter.join(teams[0])}\nTeam B: {delimiter.join(teams[1])}")

    @commands.command(name="madgab", aliases=["mg"])
    async def madgab(self, ctx):
        random_prompt = random.choice(list(prompts))
        random_prompt_answer = prompts[random_prompt]
        await ctx.send(random_prompt.title())
        return await ctx.send(f"Answer: ||{random_prompt_answer}||")


def setup(bot):
    bot.add_cog(RandomCommands(bot))
