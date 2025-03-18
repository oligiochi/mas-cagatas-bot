import os
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import humanize
import os
import discord
from discord import app_commands
import logging

class cogsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.on_error = self.on_tree_error
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("cogsManager.py is ready")
        
    #Slash Command: Reload
    #file:discord.Attachment serve a droppare un file al interno
    def add_choices_to_command(folder_path: str):
        files = [file_name for file_name in os.listdir(folder_path) if file_name.endswith(".py") and os.path.isfile(os.path.join(folder_path, file_name))]
        choices = [app_commands.Choice(name=file.removesuffix(".py"), value=f"{os.path.basename(folder_path)}.{file.removesuffix(".py")}") for file in files]
        return choices

    @app_commands.command(name='reload', description="Reload a specific module.")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(cogs=add_choices_to_command("./Cogs"))
    async def reload(self, interaction:discord.Interaction,cogs:app_commands.Choice[str]):
        logger = logging.getLogger(__name__ + '.reload')
        logger.setLevel(logging.DEBUG)
        try:
            await self.bot.reload_extension(cogs.value)
            await interaction.response.send_message(f"Module {cogs.name} reloaded successfully.",ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error reloading {cogs.name}:\n```{type(e).__name__} - {e}```",ephemeral=True)
            logger.exception(f"Error reloading {cogs.name}")
    
    #Gestore Globale degli errori
    async def on_tree_error(self,interaction: discord.Interaction, error: app_commands.AppCommandError):
        logger = logging.getLogger(__name__ + '.on_tree_error')
        logger.setLevel(logging.DEBUG)
        if isinstance(error, app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f"Command is currently on cooldown! Try again in {humanize.precisedelta(datetime.timedelta(seconds=error.retry_after), format="%.0f")}!",ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):
            return await interaction.response.send_message(f"You're missing permissions to use that Try contacting a: {error.missing_permissions}",ephemeral=True)
        elif isinstance(error, app_commands.MissingAnyRole):
            return await interaction.response.send_message(f"You don't have the adapted role for this command you need to be a: {error.missing_roles}",ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            return await interaction.response.send_message(f"{error}",ephemeral=True)
        else:
            logger.exception(f"General Error")
            return await interaction.response.send_message(f"Error: {error}",ephemeral=True)

async def setup(bot):
    await bot.add_cog(cogsManager(bot))
