import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="link")
    @app_commands.describe(code="link code")
    async def link(self, interaction: discord.Interaction, code: str):
        url = (
            "http://koti.frii.site:8000/discord/link"
            f"?code={code}&discord_id={interaction.user.id}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:
                await interaction.response.send_message(
                    str(resp.status),
                    ephemeral=True
                )
async def setup(bot):
    await bot.add_cog(general(bot))