import discord
from discord.ext import commands
from discord_components import *
from pymongo import MongoClient
import os

bot = commands.Bot(command_prefix = "!", intents = discord.Intents(messages = True, guild_messages = True, members = True, guilds = True))
cluster = MongoClient("mongodb+srv://Jaxee:zB3DV6wTS24m6MH@cluster0.2pfpp.mongodb.net/bebra?retryWrites=true&w=majority")
collection = cluster.bebra.bebra_coll
bot.remove_command('help')


@bot.event
async def on_ready():
	print("Bot connected to the server")
	DiscordComponents(bot)
	while True:
		  await bot.change_presence( status=discord.Status.online, activity=discord.Game( "Нюхает бебру" ) )
	
	for guild in bot.guilds:
		for member in guild.members:
			post = {
				"_id": member.id,
				"balance": 0,
				"xp": 0,
				"lvl": 1
			}

			if collection.count_documents({"_id": member.id}) == 0:
				collection.insert_one(post)

@bot.event
async def on_member_join(member):
	post = {
		"_id": member.id,
		"balance": 0,
		"xp": 0,
		"lvl": 1
	}

	if collection.count_documents({"_id": member.id}) == 0:
		collection.insert_one(post)


@bot.event
async def on_command_error(ctx, error):
	print(error)	

	if isinstance(error, commands.UserInputError):
		await ctx.send(embed = discord.Embed(
			description = f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`"
		))

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")


bot.run("OTE4MTA1NzI2MTk3NTgzODcy.YbCalg.CuueMPsehi1_8vwy1J5VkjaTbog")
