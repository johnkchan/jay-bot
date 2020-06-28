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

        PARAMS = {"api_key": os.environ["GIPHY_API_KEY"],
                  "tag": searchTerm}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)
            return

        data = r.json()

        if data["data"]:
            return await ctx.send(data["data"]["images"]["original"]["url"])

    @commands.command(name="weather", description="Jay Bot tells you the weather forecast", help="Shows latest weather forecast", aliases=["weatherc"])
    async def weather(self, ctx, *, location="New York City"):

        command = ctx.message.content

        #  Should return temperature in Celsius if user specifies weatherc command
        units = "metric" if ".weatherc" in command else "imperial"
        scale = "C" if ".weatherc" in command else "F"
        speed = "mps" if ".weatherc" in command else "mph"

        URL = "http://api.openweathermap.org/data/2.5/weather?"

        PARAMS = {"appid": os.getenv('OPENWEATHER_API_KEY'),
                  "q": location,
                  "units": units}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)
            return

        data = r.json()

        # Convert Latitude & Longitude to Float
        latitude = float(data['coord']['lat'])
        longitude = float(data['coord']['lon'])

        embed = discord.Embed(
            title=data["name"],
            description=f"[{latitude}{'N' if latitude > 0 else 'S'},{longitude}{'W' if latitude < 0 else 'E'}](https://www.google.com/maps/search/{latitude},{longitude}/)"
        )

        embed.add_field(
            name="Weather", value=data["weather"][0]["description"].title(), inline=False)

        embed.add_field(
            name="Temp", value=f"{int(data['main']['temp'])}°{scale}", inline=True)
        embed.add_field(
            name="Feels Like", value=f"{int(data['main']['feels_like'])}°{scale}", inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)

        embed.add_field(
            name="Humidity", value=f"{int(data['main']['humidity'])}%", inline=True)
        embed.add_field(
            name="Wind Speed", value=f"{data['wind']['speed']}{speed}", inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)

        # Convert Unix time to Readable Date Format
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.fromtimestamp(data["sys"]["sunset"])

        embed.add_field(
            name="Sunrise", value=sunrise.strftime('%I:%M %p'), inline=True)
        embed.add_field(
            name="Sunset", value=sunset.strftime('%I:%M %p'), inline=True)
        embed.add_field(
            name="\uFEFF", value="\uFEFF", inline=True)

        return await ctx.send(embed=embed)

    @commands.command(name="movie", description="Jay Bot tells you movie details", help="Shows movie details")
    async def movie(self, ctx, *, movieTitle):
        URL = "http://www.omdbapi.com/?"

        PARAMS = {"apikey": os.environ["OMDB_API_KEY"],
                  "t": movieTitle}

        try:
            r = requests.get(url=URL, params=PARAMS)
        except Exception as e:
            print(e)
            return

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

            return await ctx.send(embed=embed)

        return await ctx.send("Movie title not found")

    @commands.command(name="urbandict", description="Jay Bot tells you the definition", aliases=["urban"], help="Shows urban dictionary results")
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

        return await ctx.send(embed=embed)

    @commands.command(name="funfact", description="Jay Bot tells you a fun fact", help="Shows random fun fact")
    async def funfact(self, ctx):
        URL = "https://uselessfacts.jsph.pl/random.json?language=en"
        r = requests.get(url=URL)
        data = r.json()
        return await ctx.send(data["text"])

    @commands.command(name="joke", description="Jay Bot tells you a joke", help="Shows random joke")
    async def joke(self, ctx):
        URL = "https://official-joke-api.appspot.com/random_joke"
        r = requests.get(url=URL)
        data = r.json()
        return await ctx.send(f"{data['setup']}\n> {data['punchline']}")

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

        if outputLanguage == "zh-cn":
            pronounciation = translator.translate(
                translation, dest="zh-cn").pronunciation

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

            return await ctx.send(embed=embed)

    @commands.command(name="reddit", aliases=["ah", "dh", "ph", "dank"])
    async def reddit(self, ctx):
        reddit = praw.Reddit(client_id=os.environ["REDDIT_CLIENT_ID"],
                             client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                             user_agent="Jay Bot")

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
            return await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            return

    @commands.command(name="yelp")
    async def yelp(self, ctx, category, *, location="New York City"):
        URL = "https://api.yelp.com/v3/businesses/search?"
        HEADERS = {"Authorization": f"bearer {os.getenv('YELP_API_KEY')}"}

        PARAMS = {"terms": "restaurant",
                  "categories": category,
                  "location": location,
                  "limit": 5,
                  "price": "1, 2"}

        try:
            r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
        except Exception as e:
            print(e)
            return

        topResults = r.json()

        await ctx.send(f"Top {PARAMS['limit']} Results for '{category.title()}' in {location.title()}")

        for business in topResults["businesses"]:
            embed = discord.Embed(
                title=business["name"],
                description=", ".join([i["title"]
                                       for i in business["categories"]]),
                url=business["url"]
            )

            embed.set_thumbnail(url=business["image_url"])
            embed.add_field(
                name="Address", value=business["location"]["address1"], inline=True)
            embed.add_field(
                name="City", value=business["location"]["city"], inline=True)
            embed.add_field(
                name="Zip Code", value=business["location"]["zip_code"], inline=True)
            embed.add_field(name="Price", value=business["price"], inline=True)
            embed.add_field(
                name="Rating", value=business["rating"], inline=True)
            embed.add_field(name="Review Count",
                            value=business["review_count"], inline=True)
            embed.set_footer(
                text=f"For more info, run .yelpsearch {business['id']}")

            await ctx.send(embed=embed)

    @commands.command(name="yelpsearch")
    async def yelpsearch(self, ctx, businessID):
        URL = f"https://api.yelp.com/v3/businesses/{businessID}"
        HEADERS = {"Authorization": f"bearer {os.getenv('YELP_API_KEY')}"}

        try:
            r = requests.get(url=URL, headers=HEADERS)
        except Exception as e:
            print(e)

        business = r.json()

        if r.status_code == 404:
            return await ctx.send(business["error"]["description"])

        embed = discord.Embed(
            title=business["name"],
            description=", ".join([i["title"]
                                   for i in business["categories"]]),
            url=business["url"]
        )

        embed.set_thumbnail(url=business["image_url"])

        # Display Location Details of Business
        embed.add_field(
            name="Address", value=business["location"]["address1"], inline=True)
        embed.add_field(
            name="City", value=business["location"]["city"], inline=True)
        embed.add_field(
            name="Zip Code", value=business["location"]["zip_code"], inline=True)

        # Display Price a& Rating of Business
        embed.add_field(name="Price", value=business["price"], inline=True)
        embed.add_field(
            name="Rating", value=business["rating"], inline=True)
        embed.add_field(name="Reviews",
                        value=business["review_count"], inline=True)

        # Display Transaction Types offered by Business
        embed.add_field(name="Reservation?",
                        value="✅" if "restaurant_reservation" in business["transactions"] else "❌", inline=True)
        embed.add_field(name="Delivery?",
                        value="✅" if "delivery" in business["transactions"] else "❌", inline=True)
        embed.add_field(name="Pickup?",
                        value="✅" if "pickup" in business["transactions"] else "❌", inline=True)

        operationHours = {0: ["Monday", "Closed"],
                          1: ["Tuesday", "Closed"],
                          2: ["Wednesday", "Closed"],
                          3: ["Thursday", "Closed"],
                          4: ["Friday", "Closed"],
                          5: ["Saturday", "Closed"],
                          6: ["Sunday", "Closed"]}

        # Update operationHours dictionary with startTime and endTime
        for weekday in business["hours"][0]["open"]:
            # Convert 24 Hour Format into 12 Hour Format
            openingHour = datetime.strptime(
                weekday['start'], "%H%M").strftime("%I:%M %p")
            closingHour = datetime.strptime(
                weekday['end'], "%H%M").strftime("%I:%M %p")
            operationHours[weekday["day"]
                           ][1] = f"{openingHour} - {closingHour}"

        embed.add_field(name="Hours", value="\n".join(
            [f"{value[0]}: {value[1]}" for key, value in operationHours.items()]), inline=False)
        embed.add_field(name="Is Open Now?",
                        value="✅" if business["hours"][0]["is_open_now"] else "❌", inline=False)

        # Use second available photo to avoid duplicating thumnbnail image
        if business["photos"]:
            try:
                embed.set_image(url=business["photos"][1])
            except:
                embed.set_image(url=business["photos"][0])

        return await ctx.send(embed=embed)

    @commands.command(name="dictionary", aliases=["dict"])
    async def reddit(self, ctx, word):
        URL = f"https://owlbot.info/api/v4/dictionary/{word}"

        HEADERS = {"Authorization": f"Token {os.getenv('OWLBOT_API_KEY')}"}

        try:
            r = requests.get(url=URL, headers=HEADERS)
        except Exception as e:
            print(e)

        data = r.json()

        if r.status_code == 404:
            return await ctx.send("No definition found.")

        # Take Top 3 Definitions
        length = 3 if len(data['definitions']) > 3 else len(
            data['definitions'])

        for i in range(length):

            embed = discord.Embed(
                title=data["word"].title(),
                description=data["definitions"][i]['type'].title()
            )

            embed.add_field(
                name="Definition", value=data["definitions"][i]["definition"], inline=False)

            if data["definitions"][i]["example"]:
                embed.add_field(
                    name="Example", value=data["definitions"][i]["example"], inline=False)

            if data["definitions"][i]["image_url"]:
                embed.set_thumbnail(url=data["definitions"][i]["image_url"])

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(APICommands(bot))
