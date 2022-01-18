import discord
from discord.ext import commands
from pymongo import MongoClient
import random

"""
1. balance -> вывод баланса пользователя
2. pay -> перевод денег
3. LVL-System
"""

class Экономика(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cluster = MongoClient("mongodb+srv://Jaxee:zB3DV6wTS24m6MH@cluster0.2pfpp.mongodb.net/bebra?retryWrites=true&w=majority")
		self.collection = self.cluster.bebra.bebra_coll

	@commands.Cog.listener()
	async def on_message(self, message):
		try:

			user = message.author
			data = self.collection.find_one({"_id": user.id})

			if data["xp"] == 500 + 100 * data["lvl"]:
				self.collection.update_one({"_id": user.id},
					{"$set": {"lvl": data["lvl"] + 1}})
				self.collection.update_one({"_id": user.id},
					{"$set": {"xp": 0}})

				await message.channel.send(f"{user.mention} + 1 lvl")


			else:
				self.collection.update_one({"_id": user.id},
					{"$set": {"xp": data["xp"] + 25}})

		except Exception as e:
			post = {
				"_id": message.author.id,
				"balance": 0,
				"xp": 0,
				"lvl": 1
			}

			if self.collection.count_documents({"_id": message.author.id}) == 0:
				self.collection.insert_one(post)

	@commands.command(
		name = "баланс",
		aliases = ["balance", "cash"],
		description = "Вывод баланса пользователя",
		case_insensitive=True
	)
	async def user_balance(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = f"Баланс пользователя __{ctx.author}__: **{self.collection.find_one({'_id': ctx.author.id})['balance']}**"
			))
		else:
			await ctx.send(embed = discord.Embed(
				description = f"Баланс пользователя __{member}__: **{self.collection.find_one({'_id': member.id})['balance']}**"
			))

	@commands.command(
		name = "уровень",
		aliases = ["lvl"],
		description = "Вывод уровня пользователя",
		case_insensitive=True
	)
	async def user_lvl(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send(embed = discord.Embed(
				description = f"Уровень пользователя __{ctx.author}__: **{self.collection.find_one({'_id': ctx.author.id})['lvl']}**, **{self.collection.find_one({'_id': ctx.author.id})['xp']}**"
			))
		else:
			await ctx.send(embed = discord.Embed(
				description = f"Уровень пользователя __{member}__: **{self.collection.find_one({'_id': member.id})['lvl']}**, **{self.collection.find_one({'_id': member.id})['xp']}**"
			))


	@commands.command(
		name = "перевод",
		aliases = ["pay", "givecash"],
		description = "Перевод монет другому пользователю",
		case_insensitive=True	
	)
	async def pay_cash(self, ctx, member: discord.Member, amount: int):
		ubalance = self.collection.find_one({"_id": ctx.author.id})["balance"]
		mbalance = self.collection.find_one({"_id": member.id})["balance"]

		if amount <= 0:
			await ctx.send(embed = discord.Embed(
				description = f"__{ctx.author}__, конечно извините меня, но проход хацкерам сегодня закрыт."
			))
		else:
			self.collection.update_one({"_id": ctx.author.id},
				{"$set": {"balance": ubalance - amount}})

			self.collection.update_one({"_id": member.id},
				{"$set": {"balance": mbalance + amount}})

			await ctx.message.add_reaction("✅")

	@commands.command(
		name = "пополнить",
		aliases = ["donate"],
		description = "Пополнить монеты",
		case_insensitive=True	
	)
	@commands.has_permissions(view_audit_log=True)
	async def donate_cash(self, ctx, member: discord.Member, amount: int):
		mbalance = self.collection.find_one({"_id": member.id})["balance"]

		if amount <= 0:
			await ctx.send(embed = discord.Embed(
				description = f"__{ctx.author}__, конечно извините меня, но проход хацкерам сегодня закрыт."
			))
		else:

			self.collection.update_one({"_id": member.id},
				{"$set": {"balance": mbalance + amount}})

			await ctx.message.add_reaction("✅")

	@commands.command(
		name = "снять",
		aliases = ["undonate"],
		description = "Снять монеты",
		case_insensitive=True	
	)
	@commands.has_permissions(view_audit_log=True)
	async def undonate_cash(self, ctx, member: discord.Member, amount: int):
		mbalance = self.collection.find_one({"_id": member.id})["balance"]

		if amount <= 0:
			await ctx.send(embed = discord.Embed(
				description = f"__{ctx.author}__, конечно извините меня, но проход хацкерам сегодня закрыт."
			))
		else:

			self.collection.update_one({"_id": member.id},
				{"$set": {"balance": mbalance - amount}})

			await ctx.message.add_reaction("✅")

def setup(bot):
	bot.add_cog(Экономика(bot))