import discord
from discord.ext import commands
listener = commands.Cog.listener


class events(commands.Cog):

	def __init__(self, client):
		self.client = client

	@listener()
	async def on_member_ban(self, server, user):
		channel = self.client.get_channel(905750890814783518)
		await channel.send(f'Пользователь {user.name} был забанен')

	@listener()
	async def on_message_unban(self, server, user):
		channel = self.client.get_channel(905750890814783518)
		await channel.send(f'Пользователь {user.name} был разбанен')


	@listener()
	async def on_member_join(self, member):
		channel = self.client.get_channel(905750890814783518)
		role1 = member.guild.get_role(905749145984323637)
		await member.add_roles(role1)
		await channel.send(f"Добро пожаловать, {member.name}!")
	@listener()
	async def on_member_remove(self, member):
		channel = self.client.get_channel(905750890814783518)
		await channel.send(f"{member.name} Покинул нас!")

	@listener()
	async def on_button_click(self, res):
		await res.respond(type=6)

def setup(client):
	client.add_cog(events(client))