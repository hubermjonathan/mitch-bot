import os
import math
from time import time
import asyncio
import redis
import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Economy(bot))


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redis = redis.from_url(os.environ.get('REDIS_URL'))

    async def send_balance(self, payload):
        balance = self.redis.hget(payload.member.id, 'points').decode('utf-8')
        await payload.member.send(f'your current balance is **{balance} dining dollars** 💵')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot or (before.channel is not None and after.channel is not None):
            return

        if before.channel is None:
            self.redis.hset(member.id, 'start_time', time())

        elif after.channel is None:
            start_time = self.redis.hget(member.id, 'start_time').decode('utf-8')
            old_points = float(self.redis.hget(member.id, 'points').decode('utf-8'))
            new_points = math.floor((time() - float(start_time)) / 5)
            self.redis.hset(member.id, 'points', old_points + new_points)

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        balance = self.redis.hget(ctx.author.id, 'points').decode('utf-8')
        if float(balance) < 20:
            await ctx.message.add_reaction('👎')
            return

        await member.edit(mute=True)
        await asyncio.sleep(60)
        await member.edit(mute=False)
