import os
import math
from time import time
import asyncio
import redis
import discord
from discord.ext import tasks, commands


def setup(bot):
    economy = Economy(bot)
    bot.add_cog(economy)
    economy.count_points.start()
    economy.update_points.start()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis = redis.from_url(os.environ.get('REDIS_URL'))
        self.default_role_id = int(os.getenv('DEFAULT_ROLE_ID'))
        self.redis.delete(196141424318611457)

    @tasks.loop(seconds=5)
    async def count_points(self):
        guild = self.bot.get_guild(378759761073668096)
        for vc in guild.voice_channels:
            for m in vc.members:
                if m.bot or guild.get_role(self.default_role_id) in m.roles:
                    continue

                if self.redis.hget(m.id, 'points') is None:
                    self.redis.hset(m.id, 'points', 0)

                old_points = float(self.redis.hget(m.id, 'points').decode('utf-8'))
                self.redis.hset(m.id, 'points', old_points + 1)

    @tasks.loop(minutes=5)
    async def update_points(self):
        guild = self.bot.get_guild(378759761073668096)
        for vc in guild.voice_channels:
            for m in vc.members:
                if m.bot or guild.get_role(self.default_role_id) in m.roles:
                    continue

                if self.redis.hget(m.id, 'points_message_id') is None:
                    balance = float(self.redis.hget(m.id, 'points').decode('utf-8'))
                    await m.create_dm()
                    message = await m.send(f'your current balance is **{balance} dining dollars** 💵')
                    self.redis.hset(m.id, 'points_message_id', message.id)

                points_message_id = int(self.redis.hget(m.id, 'points_message_id').decode('utf-8'))
                points_message = await m.dm_channel.fetch_message(points_message_id)
                balance = float(self.redis.hget(m.id, 'points').decode('utf-8'))
                await points_message.edit(content=f'your current balance is **{balance} dining dollars** 💵', suppress=True)

    @count_points.before_loop
    @update_points.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        balance = float(self.redis.hget(ctx.author.id, 'points').decode('utf-8'))
        if balance/5 < 2160:
            await ctx.message.add_reaction('👎')
            return
        await ctx.message.add_reaction('👍')

        old_points = float(self.redis.hget(member.id, 'points').decode('utf-8'))
        self.redis.hset(member.id, 'points', old_points - 2160)

        await member.edit(mute=True)
        await asyncio.sleep(60)
        await member.edit(mute=False)