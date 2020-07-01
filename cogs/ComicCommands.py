import discord
from discord.ext import commands
from imgurpython import ImgurClient
import requests
import random
import os


class ComicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cyanide", aliases=["ch"])
    async def cyanide(self, ctx):
        client_id = os.getenv("IMGUR_CLIENT_ID")
        client_secret = os.getenv("IMGUR_CLIENT_SECRET")
        client = ImgurClient(client_id, client_secret)

        galleries = ["Q28iX", "F3MUq", "Hs78vjZ",
                     "4irAcqH", "XyPBv", "ytSSEEo"]
        images = client.get_album_images(random.choice(galleries))

        randomIdx = random.randrange(0, len(images))
        randomComic = images[randomIdx].link

        embed = discord.Embed(
            title="Cyanide & Happiness",
            url="http://explosm.net/"
        )

        embed.set_image(url=randomComic)

        await ctx.send(embed=embed)

    @commands.command(name="loading", aliases=["la"])
    async def loading(self, ctx):
        client_id = os.getenv("IMGUR_CLIENT_ID")
        client_secret = os.getenv("IMGUR_CLIENT_SECRET")
        client = ImgurClient(client_id, client_secret)

        galleries = ["eqog8N3", "V4983", "nk7dK", "J5hdR"]
        images = client.get_album_images(random.choice(galleries))

        randomIdx = random.randrange(0, len(images))
        randomComic = images[randomIdx].link

        embed = discord.Embed(
            title="Loading Artist",
            url="https://loadingartist.com/"
        )
        embed.set_image(url=randomComic)

        await ctx.send(embed=embed)

    @commands.command(name="lovenstein", aliases=["mrl"])
    async def lovenstein(self, ctx):
        client_id = os.getenv("IMGUR_CLIENT_ID")
        client_secret = os.getenv("IMGUR_CLIENT_SECRET")
        client = ImgurClient(client_id, client_secret)

        galleries = ["6h7o9", "MhDJD", "Spqb6Oj", "Fm9cQ"]
        images = client.get_album_images(random.choice(galleries))

        randomIdx = random.randrange(0, len(images))
        randomComic = images[randomIdx].link

        embed = discord.Embed(
            title="MrLovenstein",
            url="https://www.mrlovenstein.com/"
        )
        embed.set_image(url=randomComic)

        await ctx.send(embed=embed)

    @commands.command(name="owlturd", aliases=["ot"])
    async def owlturd(self, ctx):
        client_id = os.getenv("IMGUR_CLIENT_ID")
        client_secret = os.getenv("IMGUR_CLIENT_SECRET")
        client = ImgurClient(client_id, client_secret)

        galleries = ["KQELY", "MJBPd"]
        images = client.get_album_images(random.choice(galleries))

        randomIdx = random.randrange(0, len(images))
        randomComic = images[randomIdx].link

        embed = discord.Embed(
            title="Owl Turd",
            url="https://www.gocomics.com/shen-comix"
        )
        embed.set_image(url=randomComic)

        await ctx.send(embed=embed)

    @commands.command(name="xkcd")
    async def xkcd(self, ctx):
        randomComicNum = random.randrange(1, 2327)
        URL = f"https://xkcd.com/{randomComicNum}/info.0.json"

        try:
            r = requests.get(url=URL)
        except Exception as e:
            print(e)
            return

        comic = r.json()

        embed = discord.Embed(
            title=comic["title"],
            description=comic["alt"]
        )

        embed.set_image(url=comic["img"])
        embed.set_footer(text=f"xkcd comic #{comic['num']}")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ComicCommands(bot))
