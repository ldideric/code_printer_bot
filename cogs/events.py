import discord
from discord.ext import commands

class Events(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		activity = discord.Game(name="?git [path] --format [language]")
		await self.client.change_presence(status=discord.Status.online, activity=activity)
		print('Bot is ready.')

def setup(client):
	client.add_cog(Events(client))
