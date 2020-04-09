import discord
from discord.ext import commands
import requests
import json
import re

with open('./info.json') as json_file:
	info = json.load(json_file)

class Git(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	async def info(self, ctx):
		if ctx.guild is not None:
			await ctx.send(f"{ctx.author.mention}\nA Private Message has been sent with information!")
		embed = discord.Embed(
			title = info[0]['title'],
			description = info[0]['message'],
			colour = discord.Colour.blue()
		)
		await ctx.author.send(embed=embed)

	@commands.command()
	async def git(self, ctx, *, message):
		flags = re.findall("(\s*(?P<repo>[^\s^\/]*/[^\s^\/]*/)(?P<dir>[^\s]+))|(?P<flags>\s+--(?P<flag>[^\s]*)\s+(?P<val>[^-]*[^-\s]))", message)
		format_str = ""
		branch = ""
		for i, flag in enumerate(flags):
			if flag[4] == "format":
				if not format_str:
					format_str = flag[5]
				else:
					await ctx.send('Two format flags!')
					return
			elif flag[4] == "branch":
				if not branch:
					branch = flag[5]
				else:
					await ctx.send('Two branch flags!')
					return
		if not branch:
			branch = "master"
		r = requests.get(f"https://raw.githubusercontent.com/{flags[0][1]}{branch}/{flags[0][2]}")
		if not r:
			await ctx.send("Link does not seem to exist! Check if flags are correct!")
			return
		if not format_str:
			format_str = flags[0][2][flags[0][2].rfind('.') + 1:]
			if format_str.rfind('/') == -1:
				format_str = flags[0][2][flags[0][2].rfind('.') + 1:]
				if format_str == 's':
					format_str = 'x86asm'
			else:
				format_str = flags[0][2][flags[0][2].rfind('/') + 1:]
		if len(r.text) > 1950:
			await ctx.send(f"{ctx.author.mention} File is too long! SpAm InCoMiNg!!1!")
			index_start = 0
			while (len(r.text[index_start:]) > 1950):
				index_end = r.text.rfind("\n", index_start, index_start + 1950)
				printer = f"```{format_str}\n{r.text[index_start:index_end]}```"
				await ctx.send(printer)
				index_start = index_end
			index_end = r.text.rfind("\n", index_start, len(r.text[index_start:]))
			printer = f"```{format_str}\n{r.text[index_start:index_end]}```"
			await ctx.send(printer)
		else:
			await ctx.send(f'```{format_str}\n{r.text[:1950]}```')

def setup(client):
	client.add_cog(Git(client))
