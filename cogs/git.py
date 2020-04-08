import discord
from discord.ext import commands
import requests
import re

class Git(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def git(self, ctx, *, message):
		flags = re.findall("\s*(?P<repo>[^\s^/]*/[^\s^/]*)(?P<dir>/[^\s]*)\s+--format\s+(?P<syntax>[-]?[^-]*[^-\s])", message)
		r = requests.get(f"https://raw.githubusercontent.com/{flags[0][0]}/master{flags[0][1]}")
		if not r:
			await ctx.send("Something went wrong!")
		elif len(r.text) > 1950:
			await ctx.send(f"{ctx.author.mention}File is too long! SpAm InCoMiNg!!1!")
			index_start = 0
			while (len(r.text[index_start:]) > 1950):
				index_end = index_start + r.text.rfind("\n", index_start, index_start + 1950)
				printer = f"```{flags[0][2]}\n{r.text[index_start:index_end]}```"
				await ctx.send(printer)
				index_start = index_end
			index_end = index_start + r.text.rfind("\n", index_start, index_start + 1950)
			printer = f"```{flags[0][2]}\n{r.text[index_start:index_end]}```"
			await ctx.send(printer)
		else:
			await ctx.send(f'```{flags[0][2]}\n{r.text[:1950]}```')

def setup(client):
	client.add_cog(Git(client))
