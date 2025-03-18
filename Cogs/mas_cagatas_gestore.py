import discord
import datetime
from discord.utils import get
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dateutil.relativedelta import relativedelta
from discord import app_commands

class Mas_cagatas_gestore(commands.Cog):
    scheduler = AsyncIOScheduler()  # Define scheduler as a class attribute
    fine : datetime
    inizio: datetime
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("mas_cagatas_gestore.py is ready")
    
    @app_commands.command(name='mas_cagatas',description='Inizia una gara di mas_cagatas')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(unita=[app_commands.Choice(name='month',value='months'),app_commands.Choice(name='week',value='weeks'),app_commands.Choice(name='day',value='days'),app_commands.Choice(name='hour',value='hours')])
    async def start(self,interaction:discord.Interaction,unita:app_commands.Choice[str],value:int):
          Mas_cagatas_starter_instanze=self.bot.get_cog('Mas_cagatas_starter')
          self.inizio=datetime.datetime.now()
          self.fine=self.inizio+relativedelta(**{unita.value: value})
          sched=self.scheduler
          role=get(interaction.guild.roles, name="Mas_cagatores")
          channel=get(interaction.guild.channels, name="mas_cagatas")
          id=interaction.guild
          if Mas_cagatas_starter_instanze:
              if not (sched.running):
                await Mas_cagatas_starter_instanze.Mas_cagatas(interaction,self.inizio,self.fine,id)
                await self.startLoop(interaction)
                sched.add_job(self.stopLoop, 'date', run_date=self.fine)
                sched.start()
              else:
                await interaction.response.send_message("Esiste già una gara in corso", ephemeral=True)
            
    async def startLoop(self,interaction:discord.Interaction):
        print("start loop")
        Mas_cagatas_time_instanze=self.bot.get_cog('MasCagatasTime')
        if Mas_cagatas_time_instanze:
            Mas_cagatas_time_instanze.Category=get(interaction.guild.categories, name="Mas_cagatas")
            if self.fine:
                Mas_cagatas_time_instanze.inizio=self.inizio
                Mas_cagatas_time_instanze.fine=self.fine
            Mas_cagatas_time_instanze.aggiornaTempo.start()
            if not Mas_cagatas_time_instanze.aggiornaTempo.is_running():
                print("non è partito")
            else:
                print("è partito")

    async def stopLoop(self):
        Mas_cagatas_time_instanze=self.bot.get_cog('Mas_cagatas_time')
        if Mas_cagatas_time_instanze:
            Mas_cagatas_time_instanze.aggiornaTempo.stop()
            
async def setup(bot):
    await bot.add_cog(Mas_cagatas_gestore(bot))