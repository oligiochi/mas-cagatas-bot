import discord
from discord.ext import commands
from discord.utils import get
class Mas_cagatas_creatore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("mas_cagatas_creatore.py is ready")
        
    async def creare_channel(self,guild):
        role=get(guild.roles, name="Mas_cagatores")
        channel=get(guild.channels, name="mas_cagatas")
        category=get(guild.categories, name="Mas_cagatas")
        timer=await self.trova_time(category)
        
        if not role:
            role=await guild.create_role(name='Mas_cagatores')
        if not category and role:
            category=await guild.create_category_channel(name="Mas_cagatas",overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False),role: discord.PermissionOverwrite(read_messages=True)})
        if not channel and category:
            await guild.create_text_channel('mas_cagatas',category=category)
        if not timer and category:
            await guild.create_voice_channel('tempo',category=category,overwrites={guild.default_role: discord.PermissionOverwrite(connect=False,view_channel=False),role: discord.PermissionOverwrite(connect=False,view_channel=True)})
    
    async def trova_time(self,category):
        if category:
            for channel in category.channels:
                if channel.name.startswith("tempo"):
                    return channel  
    
async def setup(bot):
    await bot.add_cog(Mas_cagatas_creatore(bot)) 