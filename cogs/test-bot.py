import discord
from discord.ext import commands
import emoji



midjourney_bot_id = 936929561302675456
arcana_react_bot_id = 1248848353106726974

reaction_blocked_users = [arcana_react_bot_id]
reaction_enabled_users = {midjourney_bot_id}

# print('react-bot loaded')
print(f'cog test-bot.py has been loaded')

class TestBot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.default_reactions = ["🔥", "1️⃣", "2️⃣", "3️⃣", "4️⃣"]
    self.reactions = {}

  # --------------------------------------------------

  @commands.command(name="test2")
  async def test_test(self, ctx):
    if ctx.author == self.bot.user:
      return
    
    print('performing test2 on cogs.test-bot.py')

    await ctx.channel.send('test successful from cogs.test-bot.py')
    # print(f'test 2 successful')




async def setup(bot):
  await bot.add_cog(TestBot(bot))