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
            "http://beta.frii.site/discord/link"
            f"?code={code}&discord_id={interaction.user.id}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:
                if resp.status == 200:
                    await interaction.response.send_message(
                        "Successfully linked account!",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"Failed to link account with status code: {resp.status}. Please contact support (or ping me @ctih)",
                        ephemeral=True
                    )

async def setup(bot):
    await bot.add_cog(general(bot))