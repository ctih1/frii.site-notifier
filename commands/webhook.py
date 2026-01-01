import discord
from discord.ext import commands
from aiohttp import web
import json

class notify_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.app = web.Application()
        self.app.router.add_post("/api/notify", self.handle_notify)
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

        embed = discord.Embed(title="login notification")
        embed.add_field(name="ip", value=data.get("ip", "unknown"), inline=False)
        embed.add_field(name="user_agent", value=data.get("user-agent", "unknown"), inline=False)
        embed.add_field(name="success", value=str(data.get("success")), inline=True)
        embed.add_field(name="mfa_triggered", value=str(data.get("mfa-triggered")), inline=True)
        embed.add_field(name="login_type", value=data.get("login-type"), inline=True)
        embed.add_field(name="login_stage", value=data.get("login-stage"), inline=True)

        try:
            await user.send(embed=embed)
        except:
            return web.Response(status=403)

        return web.Response(status=204)

async def setup(bot):
    await bot.add_cog(notify_api(bot))
