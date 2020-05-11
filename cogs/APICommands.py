import discord
from discord.ext import commands
from googletrans import Translator
from datetime import datetime
import random
import praw
import requests
import os


class APICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gif", description="It's so fluffy!")
    async def gif(self, ctx, *, searchTerm):
        URL = "http://api.giphy.com/v1/gifs/random?"
        api_key = os.environ["GIPHY_API_KEY"]

        PARAMS = {"api_key": api_key,
                  "tag": searchTerm}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)

        data = r.json()

        if data["data"]:
            await ctx.send(data["data"]["images"]["original"]["url"])

    @commands.command(name="weather", description="jay_bot tells you the weather forecast", help="Shows latest weather forecast", aliases=["sunrise", "sunset", "weatherc"])
    async def weather(self, ctx, *, location="New York City"):

        command = ctx.message.content
        units = "metric" if command == ".weatherc" else "imperial"
        measurement = "C" if command == ".weatherc" else "F"
        speed = "mps" if command == ".weatherc" else "mph"

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        api_key = os.getenv('OPENWEATHER_API_KEY')
        PARAMS = {"appid": api_key,
                  "q": location,
                  "units": units}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)

        data = r.json()

        # Convert Unix time to Readable Date Format
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(data["sys"]["sunset"])

        embed = discord.Embed(
            title=data["name"]
        )

        embed.add_field(
            name="Weather", value=data["weather"][0]["description"].title(), inline=False)
        embed.add_field(
            name="Temp", value=f"{int(data['main']['temp'])}°{measurement}", inline=True)
        embed.add_field(
            name="Feels Like", value=f"{int(data['main']['feels_like'])}°{measurement}", inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)
        embed.add_field(
            name="Humidity", value=f"{int(data['main']['humidity'])}%", inline=True)
        embed.add_field(
            name="Wind Speed", value=f"{data['wind']['speed']}{speed}", inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)
        embed.add_field(
            name="Sunrise", value=sunrise.strftime('%I:%M %p'), inline=True)
        embed.add_field(
            name="Sunset", value=sunset.strftime('%I:%M %p'), inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)

        embed.set_footer(
            text=f"lat: {data['coord']['lat']} | lon: {data['coord']['lon']}")

        await ctx.send(embed=embed)

    @commands.command(name="movie", description="jay_bot tells you movie details", help="Shows movie details")
    async def movie(self, ctx, *, movieTitle):
        URL = "http://www.omdbapi.com/?"

        PARAMS = {"apikey": os.environ["OMDB_API_KEY"],
                  "t": movieTitle}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)

        data = r.json()

        if data["Response"] == "True":
            embed = discord.Embed(
                title=data["Title"],
                url=f"https://www.imdb.com/title/{data['imdbID']}"
            )

            embed.set_thumbnail(url=data["Poster"])
            embed.add_field(
                name="Plot", value=data["Plot"], inline=False)
            embed.add_field(
                name="Genre", value=data["Genre"], inline=False)
            embed.add_field(
                name="Director", value=data["Director"], inline=False)
            embed.add_field(name="Actors", value=data["Actors"], inline=False)
            if data["Awards"] != "N/A":
                embed.add_field(
                    name="Awards", value=data["Awards"], inline=False)
            embed.add_field(
                name="Metascore", value=data["Metascore"], inline=True)
            embed.add_field(
                name="imdb Rating", value=data["imdbRating"], inline=True)
            embed.add_field(
                name="imdb Votes", value=data["imdbVotes"], inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("movie not found >:")

    @commands.command(name="urbandict", description="jay_bot tells you the definition", aliases=["urban"], help="Shows urban dictionary results")
    async def urbandict(self, ctx, *, searchTerm):
        URL = "http://api.urbandictionary.com/v0/define?"
        PARAMS = {"term": searchTerm}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)

        data = r.json()
        topResult = data["list"][0]

        embed = discord.Embed(
            title=topResult["word"].title(),
            url=topResult["permalink"]
        )

        embed.set_thumbnail(
            url="https://img.pngio.com/urban-dictionary-definition-for-your-fave-urban-dictionary-png-670_315.png")
        embed.add_field(
            name="Author", value=topResult["author"], inline=False)
        embed.add_field(
            name="Definition", value=topResult["definition"], inline=False)
        embed.add_field(
            name="Example", value=topResult["example"], inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="funfact", description="jay_bot tells you a fun fact", help="Shows random fun fact")
    async def funfact(self, ctx):
        URL = "https://uselessfacts.jsph.pl/random.json?language=en"
        r = requests.get(url=URL)
        data = r.json()
        await ctx.send(data["text"])

    @commands.command(name="joke", description="jay_bot tells you a joke", help="Shows random joke")
    async def joke(self, ctx):
        URL = "https://official-joke-api.appspot.com/random_joke"
        r = requests.get(url=URL)
        data = r.json()
        await ctx.send(f"{data['setup']}\n> {data['punchline']}")

    @commands.command(name="translate", help="Shows translation")
    async def translate(self, ctx, *, text):

        LANGUAGES = {
            'af': 'afrikaans',
            'sq': 'albanian',
            'am': 'amharic',
            'ar': 'arabic',
            'hy': 'armenian',
            'az': 'azerbaijani',
            'eu': 'basque',
            'be': 'belarusian',
            'bn': 'bengali',
            'bs': 'bosnian',
            'bg': 'bulgarian',
            'ca': 'catalan',
            'ceb': 'cebuano',
            'ny': 'chichewa',
            'zh-cn': 'chinese (simplified)',
            'zh-tw': 'chinese (traditional)',
            'co': 'corsican',
            'hr': 'croatian',
            'cs': 'czech',
            'da': 'danish',
            'nl': 'dutch',
            'en': 'english',
            'eo': 'esperanto',
            'et': 'estonian',
            'tl': 'filipino',
            'fi': 'finnish',
            'fr': 'french',
            'fy': 'frisian',
            'gl': 'galician',
            'ka': 'georgian',
            'de': 'german',
            'el': 'greek',
            'gu': 'gujarati',
            'ht': 'haitian creole',
            'ha': 'hausa',
            'haw': 'hawaiian',
            'iw': 'hebrew',
            'hi': 'hindi',
            'hmn': 'hmong',
            'hu': 'hungarian',
            'is': 'icelandic',
            'ig': 'igbo',
            'id': 'indonesian',
            'ga': 'irish',
            'it': 'italian',
            'ja': 'japanese',
            'jw': 'javanese',
            'kn': 'kannada',
            'kk': 'kazakh',
            'km': 'khmer',
            'ko': 'korean',
            'ku': 'kurdish (kurmanji)',
            'ky': 'kyrgyz',
            'lo': 'lao',
            'la': 'latin',
            'lv': 'latvian',
            'lt': 'lithuanian',
            'lb': 'luxembourgish',
            'mk': 'macedonian',
            'mg': 'malagasy',
            'ms': 'malay',
            'ml': 'malayalam',
            'mt': 'maltese',
            'mi': 'maori',
            'mr': 'marathi',
            'mn': 'mongolian',
            'my': 'myanmar (burmese)',
            'ne': 'nepali',
            'no': 'norwegian',
            'ps': 'pashto',
            'fa': 'persian',
            'pl': 'polish',
            'pt': 'portuguese',
            'pa': 'punjabi',
            'ro': 'romanian',
            'ru': 'russian',
            'sm': 'samoan',
            'gd': 'scots gaelic',
            'sr': 'serbian',
            'st': 'sesotho',
            'sn': 'shona',
            'sd': 'sindhi',
            'si': 'sinhala',
            'sk': 'slovak',
            'sl': 'slovenian',
            'so': 'somali',
            'es': 'spanish',
            'su': 'sundanese',
            'sw': 'swahili',
            'sv': 'swedish',
            'tg': 'tajik',
            'ta': 'tamil',
            'te': 'telugu',
            'th': 'thai',
            'tr': 'turkish',
            'uk': 'ukrainian',
            'ur': 'urdu',
            'uz': 'uzbek',
            'vi': 'vietnamese',
            'cy': 'welsh',
            'xh': 'xhosa',
            'yi': 'yiddish',
            'yo': 'yoruba',
            'zu': 'zulu',
            'fil': 'Filipino',
            'he': 'Hebrew'
        }

        translator = Translator()

        detection = translator.detect(text)
        language = detection.lang.lower()
        confidence = detection.confidence

        outputLanguage = "zh-cn" if language == "en" else "en"
        output = translator.translate(text, dest=outputLanguage)
        translation = output.text
        pronounciation = translator.translate(
            text, dest=language).pronunciation

        if translation:

            embed = discord.Embed(
                colour=discord.Colour.blue()
            )

            embed.add_field(
                name="Translation", value=translation, inline=False)

            if pronounciation:
                embed.add_field(
                    name="Pronounciation", value=pronounciation, inline=False)

            embed.add_field(
                name="Detected", value=f"{LANGUAGES[language].title()}", inline=True)
            embed.add_field(
                name="Confidence", value=f"{confidence}", inline=True)

            await ctx.send(embed=embed)

    @commands.command(name="reddit", aliases=["ah", "dh", "ph", "dank"])
    async def reddit(self, ctx):
        reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                             client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                             user_agent="jay_bot")

        subreddit_dict = {
            "ah": "accountinghumor",
            "dh": "designershumor",
            "ph": "programmerhumor",
            "dank": "memes"
        }

        command = ctx.message.content[1:]
        selection = subreddit_dict[command]

        try:
            submission = reddit.subreddit(selection).random()
            embed = discord.Embed(
                title=submission.title,
                url=submission.shortlink
            )
            embed.set_image(url=submission.url)
            msg = await ctx.send(embed=embed)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(APICommands(bot))
