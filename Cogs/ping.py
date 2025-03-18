import discord
from discord.ext import commands
from discord import app_commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ping.py is ready")

    @app_commands.command(name='ping',description='Mostra il ritardo del bot')
    async def ping(self, ctx):
        ritardo = round(self.bot.latency * 1000)
        await ctx.send(f'Pong!\n{ritardo} ms\nCiao {ctx.author.mention}!')

async def setup(bot):
    await bot.add_cog(ping(bot))
