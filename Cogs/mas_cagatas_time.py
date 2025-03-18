import discord
import datetime
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
from dateutil.relativedelta import relativedelta
import humanize
from discord import app_commands
class MasCagatasTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timerVocal=None
        
    timerVocal : discord.VoiceChannel
    Category : discord.CategoryChannel
    fine : datetime
    fineVariabile : datetime
    inizio: datetime
    primo = True
    @commands.Cog.listener()
    async def on_ready(self):
        print("mas_cagatas_time.py is ready")
    
    async def find_emoji(self,minuti:int):
        emoji = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚']
        return emoji[minuti//5]
    
    @tasks.loop(seconds=300)
    async def aggiornaTempo(self):
        if self.primo:
            self.fineVariabile=self.fine
            self.primo=False
        else:
            self.fineVariabile=self.fineVariabile-relativedelta(minutes=5) 
        if not self.timerVocal:
            Mas_cagatas_creatore_instanze=self.bot.get_cog('Mas_cagatas_creatore')
            if Mas_cagatas_creatore_instanze:
                self.timerVocal=await Mas_cagatas_creatore_instanze.trova_time(self.Category)
        if self.timerVocal:
            tempo_delta = self.fineVariabile - self.inizio
            tempo = f"{tempo_delta.days} Days {tempo_delta.seconds//3600}:{(tempo_delta.seconds//60)%60}"
            emoji=await self.find_emoji(int((tempo_delta.seconds//60)%60))
            new_nome = f"tempo: {emoji} {tempo}"
            try:
                await self.timerVocal.edit(name=new_nome)
            except discord.HTTPException as e:
                print(f"Errore nella modifica del nome del canale: {e}")
        
    @app_commands.command(name='tempo_restante',description='Mostra il tempo rimanente')
    @app_commands.checks.has_any_role("Mas_cagatores","mas_cagatores")
    async def tempo_restante(self,interaction:discord.Interaction):
        if not self.primo:
            await interaction.response.send_message(f'Tempo rimanente: {humanize.precisedelta(self.fine-datetime.datetime.now(),format="%.0f")}',ephemeral=True)
        else:
            await interaction.response.send_message(f'Non c\'è nessuna gara in corso',ephemeral=True) 

async def setup(bot):
    await bot.add_cog(MasCagatasTime(bot)) 
    
