import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from pymongo import MongoClient
import pymongo
import datetime

load_dotenv(find_dotenv())

Secret = os.environ["SECRET"]
MonogUri = os.environ["MONGO_URI"]

client = pymongo.MongoClient(MonogUri)
db = client.deaths
col = db["Swap Meets Deaths"]

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=".", intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.command()
async def deaths(ctx):
    em = discord.Embed(
        title="Death Tracker",
        colour=0xf7f9f2)
    for x in col.find({}, {"_id": 0}):
        em.add_field(name=x["rsn"] + " -", value="")
        em.add_field(name="PvM Deaths", value=x["PvM Deaths"])
        em.add_field(name="PvP Deaths", value=x["PvP Deaths"])
        em.timestamp = datetime.datetime.now()
    await ctx.send(embed=em)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if username == 'waste-of-time' and channel == 'he-died':
        grabUser = user_message.split()
        rsnUser = grabUser[0]
        removeAstrk = rsnUser.replace("*", "")
        queryPvMDeaths = col.find_one({}, {"_id": 0, "user": 1, "PvM Deaths": 1, "PvP Deaths": 1})
        if 'has died' in user_message:
            pvmDeaths = queryPvMDeaths["PvM Deaths"]
            result = col.update_one({'user': removeAstrk}, {'$inc': {'PvM Deaths': + 1}})
            print('Updated PvM death for: ' + removeAstrk)
        elif 'has just been killed by' in user_message:
            pvpDeaths = queryPvMDeaths["PvP Deaths"]
            result = col.update_one({'user': removeAstrk}, {'$inc': {'PvP Deaths': + 1}})
            print('Updated PvP death for: ' + removeAstrk)
    await client.process_commands(message)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    # channel = str(message.channel.name)

    if (username == 'Frosty_Dad'):
        await message.author.send('shut up')

    await client.process_commands(message)    

client.run(Secret)