from discord.ext import commands, tasks
import discord
import os
import re


client = commands.Bot(command_prefix=".")
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".help"))
    # check_time.start()
    print(f"{client.user.name} is connected to Discord.")


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     msg = message.content.lower()

#     # Override on_message default behavior of forbidding any extra commands from running
#     await client.process_commands(message)


# Load all Cog Extensions in Cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.getenv('BOT_TOKEN'))
