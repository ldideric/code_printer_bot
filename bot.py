import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '?')

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')


client.run('Njk3NDU5MDQ1MjM3NTIyNDQz.Xo5VFQ.BrnxDC9qRCYVoacMJDql0sXqppA')
