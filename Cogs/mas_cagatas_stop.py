import os
import discord
from discord.ext import commands
from discord import app_commands

class mas_cagatas_stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ping.py is ready")

    @app_commands.command(name='pong',description='Mostra il ritardo del bot')
    async def ping(self, ctx):
        ritardo = round(self.bot.latency * 1000)
        await ctx.send(f'Pong!\n{ritardo} ms\nCiao {ctx.author.mention}!')
    
    async def remove_all_commands(self):
        commands = await self.bot.application.commands()
        for command in commands:
            await self.bot.application.delete_command(command.id)
            
    @app_commands.command(name='remove_role_from_all_user',description='Rimuove un ruolo a tutti gli utenti')
    async def remove_role_from_all_user(self,interaction:discord.Interaction,role:discord.Role):
        for member in interaction.guild.members:
            if role in member.roles:
                await member.remove_roles(role)
    
    @app_commands.command(name='clear_channels',description='Pulisce tutti i canali')           
    async def clear_channels(self,interaction:discord.Interaction,channel:discord.TextChannel):
        await interaction.response.send_message(f'Pulizia canale {channel.name} in corso...',ephemeral=True)
        await channel.purge(limit=None)
    
    @app_commands.command(name='mas_cagatas_stop',description='Stoppa il torneo')
    async def mas_cagatas_stop(self,interaction:discord.Interaction,channel:discord.TextChannel,role:discord.Role):
        Mas_cagatas_contacacche_instanze=self.bot.get_cog('mas_cagatas_contacacche')
        await interaction.response.send_message('Sto stoppando il torneo...',ephemeral=True)
        print("ok1")
        await self.remove_role_from_all_user(interaction,role)
        print("ok2")
        await channel.delete()
        print("ok3")
        await Mas_cagatas_contacacche_instanze.classifica(interaction)
        print("ok4")
        

               
async def setup(bot):
    await bot.add_cog(mas_cagatas_stop(bot))
