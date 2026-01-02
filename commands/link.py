import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from datetime import datetime

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

    @app_commands.command(name="send-test")
    async def send_test(self, interaction: discord.Interaction):
        data = {
            "ip": "192.168.32.1",
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
            "success": False,
            "mfa-triggered": True,
            "login-type": "password",
            "login-stage": "session"
        }   

        embed = discord.Embed(
            title="Login Notification",
            description=f"New login activity detected for user ID `{interaction.user.id}`.",
            color=0xFF5733,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="IP Address", value=data.get("ip", "Unknown"), inline=False)
        embed.add_field(name="User Agent", value=f"```{data.get('user-agent', 'Unknown')}```", inline=False)
        embed.add_field(name="Success", value=False, inline=True)
        embed.add_field(name="2FA Triggered", value=True, inline=True)
        embed.add_field(name="Login Type", value="Username and password", inline=True)
        embed.add_field(name="\u200b", value="Authentication failure", inline=False)

        interaction.user.send(embed=embed)


async def setup(bot):
    await bot.add_cog(general(bot))