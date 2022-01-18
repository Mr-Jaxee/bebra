import discord 
from discord.ext import commands
import time
import os


intents = discord.Intents.default()
intents.members = True


client = commands.Bot( command_prefix = '!', intents = intents )

@client.event
async def on_ready():
	print( 'Ready!' )
	print( 'Logged in as ---->', client.user )
	print( 'ID:', client.user.id )

@client.event
async def on_raw_reaction_add(payload):
	channel = client.get_channel(payload.channel_id)
	message = await channel.fetch_message(payload.message_id)
	guild = client.get_guild(payload.guild_id)
	reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

	# only work if it is the client
	if payload.member.id == client.user.id:
		return

	if payload.message_id == 918009796211404820 and reaction.emoji == '🌽':
		role = discord.utils.get(guild.roles, name='Фермер')
		await payload.member.add_roles(role)
		
	if payload.message_id == 918009796211404820 and reaction.emoji == '💀':
		role = discord.utils.get(guild.roles, name='охотник за головами')
		await payload.member.add_roles(role)
		
	if payload.message_id == 918009796211404820 and reaction.emoji == '🌲':
		emoji = '✅'
		role = discord.utils.get(guild.roles, name='Лесоруб')
		await payload.member.add_roles(role)

	if payload.message_id == 918009796211404820 and reaction.emoji == '🐻':
		role = discord.utils.get(guild.roles, name='Охотник')
		await payload.member.add_roles(role)
		
	if payload.message_id == 918009796211404820 and reaction.emoji == '💧':
		role = discord.utils.get(guild.roles, name='Водо-качка')
		await payload.member.add_roles(role)
		
	if payload.message_id == 918009796211404820 and reaction.emoji == '😷':
		role = discord.utils.get(guild.roles, name='Курьер')
		await payload.member.add_roles(role)

	if payload.message_id == 918031419471699990 and reaction.emoji == '👍':
		role = discord.utils.get(guild.roles, name='Из Союзного Клана')
		await payload.member.add_roles(role)

	if payload.message_id == 918030809670221845 and reaction.emoji == '👍':
		role = discord.utils.get(guild.roles, name='Белазник')
		await payload.member.add_roles(role)

		
client.run("OTE4MTA1NzI2MTk3NTgzODcy.YbCalg.5ZM1574_Kz9pDGLxjuNXcleviBM")

