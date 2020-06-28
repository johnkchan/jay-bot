import discord
from discord.ext import commands
import random


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", description="jay_bot clears your messages")
    async def clear(self, ctx, amount=10):
        return await ctx.channel.purge(limit=amount)

    @commands.command(name="tts", description="Text-to-Speech")
    async def tts(self, ctx, *, text):
        return await ctx.send(content=text, tts=True)

    @commands.command(name="watch", description="jay_bot tells you to watch shows")
    async def watch(self, ctx, show: str = "", *, participants: str = ""):
        if show:
            show += " "

        watchers_list = [
            686979275571855392,
            334770873166725121,
            265621524851982350
        ]

        msg_author_id = ctx.message.author.id
        watchers = [
            f"<@!{str(watcher)}>" for watcher in watchers_list if watcher != msg_author_id]

        if participants:
            for i in participants:
                watchers.append(i)

        watchers = ",".join(watchers)

        if ctx.author.voice and ctx.author.voice.channel:
            # guild = ctx.message.guild
            # author = ctx.message.author
            channel = ctx.author.voice.channel
            link = await channel.create_invite(max_age=300)

            embed = discord.Embed(
                title="Watch Notification",
                description=f"{watchers} watch {show}with me on #{channel}"
            )

            await ctx.send(embed=embed)
            await ctx.send(link)
            return

        # If user is not in voice channel, notify user and end command
        return await ctx.send("you are not connected to a voice channel")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
