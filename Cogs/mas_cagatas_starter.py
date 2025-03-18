import discord
from discord.ext import commands
import datetime
from discord.ui import Button, View
from discord.utils import get
from matplotlib.dates import relativedelta
class Mas_cagatas_starter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("mas_cagatas_starter.py is ready")
        
    async def Mas_cagatas(self,interaction:discord.Interaction,inizio:datetime,fine:datetime,guild):
        embed = discord.Embed(
            title=(f'Mas cagatas CHALLENGE'),
            description=(f'La gara dura fino a {fine.year}-{fine.month}-{fine.day}'),
            colour=discord.Colour.from_rgb(122,89,1),
            timestamp=inizio
        )

        embed.set_author(
            name='Mas_cagatas_bot',
            icon_url='https://www.clipartkey.com/mpngs/m/31-313403_poop-emoji-png-poop-emoji-transparent.png'
        )
        embed.set_footer(text='La gara Ha inizio', icon_url='https://www.clipartkey.com/mpngs/m/31-313403_poop-emoji-png-poop-emoji-transparent.png')

        embed.set_thumbnail(url='https://www.clipartkey.com/mpngs/m/31-313403_poop-emoji-png-poop-emoji-transparent.png')
        
        button = Button(label="Partecipa", emoji="💩")
        button.callback = self.partecipa_callback  # Imposta la funzione di callback
        view = View()
        view.add_item(button)
                
        await interaction.response.send_message(embed=embed, view=view)
        
        Mas_cagatas_creatore_instanze=self.bot.get_cog('Mas_cagatas_creatore')
        if Mas_cagatas_creatore_instanze:
            await Mas_cagatas_creatore_instanze.creare_channel(guild)
        
            
    async def partecipa_callback(self, interaction: discord.Interaction):
        role=get(interaction.guild.roles, name="Mas_cagatores")
        if role not in interaction.user.roles:
            await interaction.response.send_message("Hai partecipato alla gara!", ephemeral=True)
            await interaction.user.add_roles(role)
            mas_cagatas_contacacche_instanze=self.bot.get_cog('mas_cagatas_contacacche')
            if mas_cagatas_contacacche_instanze:
                await mas_cagatas_contacacche_instanze.addPersona(interaction.user)
        else:
            await interaction.response.send_message("Hai già partecipato alla gara!", ephemeral=True)
async def setup(bot):
    await bot.add_cog(Mas_cagatas_starter(bot))