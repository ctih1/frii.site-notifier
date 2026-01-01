import discord
from discord.ext import commands
from aiohttp import web
import json
import datetime

class notify_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = web.Application()
        self.app.router.add_post("/api/notify", self.handle_notify)
        self.app.router.add_get("/api/test", self.handle_test)
        self.runner = web.AppRunner(self.app)
        bot.loop.create_task(self.start_server())

    async def start_server(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, "0.0.0.0", 9898)
        await site.start()
 
    async def handle_notify(self, request):
        discord_id = request.query.get("id")
        if not discord_id:
            return web.Response(status=400)

        try:
            data = await request.json()
        except:
            return web.Response(status=400)

        user = await self.bot.fetch_user(int(discord_id))
        if not user:
            return web.Response(status=404)

        if data.get("success"):
            success = "Yes"
            color = 0x1ABC9C
        else:
            success = "No"
            color = 0xFF5733
            
        mfa = "Yes" if data.get("mfa-triggered") else "No"

        login_type = "username and password"
        invalid_password = "Invalid password" if data.get("login-stage") == "password" else None

        embed = discord.Embed(
            title="Login Notification",
            description=f"New login activity detected for user ID `{discord_id}`.",
            color=0x1ABC9C,
            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(name="IP Address", value=data.get("ip", "Unknown"), inline=False)
        embed.add_field(name="User Agent", value=f"```{data.get('user-agent', 'Unknown')}```", inline=False)
        embed.add_field(name="Success", value=success, inline=True)
        embed.add_field(name="2FA Triggered", value=mfa, inline=True)
        embed.add_field(name="Login Type", value=login_type, inline=True)
        if invalid_password:
            embed.add_field(name="\u200b", value=invalid_password, inline=False)

        try:
            await user.send(embed=embed)
        except:
            return web.Response(status=403)

        return web.Response(status=204)

    async def handle_test(self, request):
        user = await self.bot.fetch_user(542701119948849163)
        if not user:
            return web.Response(status=404)

        embed = discord.Embed(
            title="Test Notification",
            description="This is a test embed.",
            color=0xFF5733,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="IP Address", value="127.0.0.1", inline=False)
        embed.add_field(name="User Agent", value="```Mozilla/5.0 (TempleOS 00.0; Tmp64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Templ/104.3.0.0 Edg/143.0.0.0```", inline=False)
        embed.add_field(name="Success", value="Yes", inline=True)
        embed.add_field(name="2FA Triggered", value="No", inline=True)
        embed.add_field(name="Login Type", value="username and password", inline=True)
        embed.add_field(name="\u200b", value="Invalid password", inline=False)

        try:
            await user.send(embed=embed)
        except:
            return web.Response(status=403)

        return web.Response(text="Test embed sent", status=200)


async def setup(bot):
    await bot.add_cog(notify_api(bot))
