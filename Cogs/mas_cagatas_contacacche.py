import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
class mas_cagatas_contacacche(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    persone_cagate={}
    persone_amonizioni={}
    numero_amonizioni=3
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("mas_cagatas_contacacche.py is ready")
        await self.load_persons_with_tag('Mas_cagatores')
        
    async def load_persons_with_tag(self, tag):
        # Carica tutte le persone con un certo tag nel dizionario
        for guild in self.bot.guilds:
            for member in guild.members:
                if tag in [role.name for role in member.roles]:
                    await self.addPersona(member)

    async def addPersona(self,persona:discord.User):
        self.persone_cagate[persona.id]=0
        self.persone_amonizioni[persona.id]=0
    
    @app_commands.command(name='mie_cagate',description='Mostra le tue cagate')
    @app_commands.checks.has_any_role("Mas_cagatores","mas_cagatores")
    @app_commands.checks.cooldown(3, 86400)
    async def mie_cagate(self,interaction:discord.Interaction):
        if not self.persone_cagate:
            await self.load_persons_with_tag('Mas_cagatores')
        user=interaction.user
        num=self.persone_cagate[interaction.user.id]
        await interaction.response.send_message(f'Le tue cagate {user} sono {num}',ephemeral=True)               

    @app_commands.command(name='classifica',description='Mostra la classifica')
    @app_commands.checks.has_any_role("Mas_cagatores","mas_cagatores")
    @app_commands.checks.cooldown(3, 86400, key=lambda i:(i.channel.id))
    @app_commands.check(lambda i: i.channel.id==get(i.guild.channels, name="mas_cagatas").id)
    async def classifica(self,interaction:discord.Interaction):
        if not self.persone_cagate:
            await self.load_persons_with_tag('Mas_cagatores')
        self.persone_cagate=dict(sorted(self.persone_cagate.items(), key=lambda x: x[1], reverse=True))
        member_names = {member_id: await self.get_member_name(interaction.guild, member_id) for member_id in self.persone_cagate.keys()}
        embed = discord.Embed(
            title=(f'Classifica'),
            colour=discord.Colour.from_rgb(122,89,1),
            description='\n'.join([f"{member_names[key]}: {value}" for key, value in self.persone_cagate.items()])
        )
        await interaction.response.send_message(embed=embed)
        
    async def get_member_name(self, guild, member_id):
        # Restituisci il nome dell'utente dato il suo ID
        member = guild.get_member(member_id)
        return member.name if member else f"Utente non trovato ({member_id})"
    
    @commands.Cog.listener()
    async def on_message(self,message):
        channel=get(message.guild.channels, name="mas_cagatas")
        if message.author != self.bot.user and message.author.id in self.persone_cagate.keys() and message.channel.id==channel.id:
            if '💩' in message.content or not '-' in message.content:
                clear_message=message.content.replace('-','')
                if all(char == '💩' for char in clear_message):
                    self.persone_cagate[message.author.id]+=clear_message.count('💩')
                    await message.channel.send(f'{message.author.mention} hai cagato {message.content.count("💩")} volte')
                else:
                    self.persone_amonizioni[message.author.id]+=1
                    await message.channel.send(f'{message.author.mention} hai cagato fuori dal vaso {self.persone_amonizioni[message.author.id]} volte')
                    if self.persone_amonizioni[message.author.id]>=self.numero_amonizioni:
                        await message.channel.send(f'{message.author.mention} sei stato squalificato')
                        await message.author.remove_roles(get(message.guild.roles, name="Mas_cagatores"))
async def setup(bot):
    await bot.add_cog(mas_cagatas_contacacche(bot))

