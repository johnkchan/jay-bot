# Jay Bot for Discord

Jay Bot interacts with Discord users through designated commands.
Users can retrieve the latest information from the various API endpoints listed below.

## Installation

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [requirements](./requirements.txt).

```bash
pip install -r requirements.txt
```

2. Request API Access from below [API](##API) providers
3. Create .env file to store API keys as environment variables

```bash
touch .env
```

## API Directory

- [GIPHY](https://developers.giphy.com/)
- [Official-Joke-API](https://official-joke-api.appspot.com/random_joke)
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

![alt text](https://i.imgur.com/wAQ4OJM.png "Dictionary Command Example")

`.yelp <category> <location>`

![alt text](https://i.imgur.com/lG8Ly7Y.png "Yelp Fusion API Command Example")

`.weather <location>`

![alt text](https://i.imgur.com/uA2uZM7.png "Open Weather API Command Example")

`.translate <searchTerm>`

![alt text](https://i.imgur.com/7U79sgM.png "Translate Command Example")

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
