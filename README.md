# Jay Bot

Jay Bot is an interactive bot that allows Discord users to retrieve the latest dataset from various API providers through designated commands.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Installation

1. Use the [pip](https://pip.pypa.io/en/stable/) package manager to install [requirements](./requirements.txt)

```bash
pip install -r requirements.txt
```

2. Request API access from the below [API](#API) providers
3. Create a .env file to store granted API keys as environment variables

```bash
touch .env
```

## API Directory

- [Advice Slip API](https://api.adviceslip.com/)
- [GIPHY](https://developers.giphy.com/)
- [Imgur](https://github.com/Imgur/imgurpython)
- [Official-Joke-API](https://official-joke-api.appspot.com/random_joke)
- [News API](https://newsapi.org/docs/get-started)
- [Open Movie Database](http://www.omdbapi.com/)
- [Open Weather Map](https://openweathermap.org/api)
- [OwlBot Dictionary API](https://owlbot.info/)
- [Reddit PRAW](https://praw.readthedocs.io/en/latest/)
- [UrbanDictionary](http://api.urbandictionary.com/v0/define?)
- [Useless Facts](https://uselessfacts.jsph.pl/random.json?language=en)
- [Yelp Fusion API](https://www.yelp.com/developers)

## Usage

```bash
python bot.py
```

## Discord Commands

A list of all Jay Bot Commands can be found by using the .help command on the Discord platform

```bash
.help
```

## Command Examples

`.dictionary <searchTerm>`

![alt text](https://i.imgur.com/v64imOS.gifv)

`.reddit <subreddit>`

![alt text](https://i.imgur.com/bn9DMzN.gifv)

`.translate <searchTerm>`

![alt text](https://i.imgur.com/sJBDwt1.gifv)

`.weather <location>`

![alt text](https://i.imgur.com/D8V7F4Z.gifv)

`.yelp <category> <location>`

![alt text](https://i.imgur.com/PsZvMhs.gifv)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
