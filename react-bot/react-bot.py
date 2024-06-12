import discord
from discord.ext import commands
import emoji



midjourney_bot_id = 936929561302675456
arcana_react_bot_id = 1248848353106726974

reaction_blocked_users = [arcana_react_bot_id]
reaction_enabled_users = {midjourney_bot_id}



class ReactBot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.default_reactions = ["🔥", "1️⃣", "2️⃣", "3️⃣", "4️⃣"]
    self.reactions = {}

  # --------------------------------------------------

  @commands.Cog.listener()
  async def on_message(self, message):
    #ignore messages sent by the bot itself to prevent a loop
    if message.author == self.bot.user:
      return
    
    # Check if the message content is "hi" (case-insensitive)
    if message.content.lower() == "hi":
      await message.channel.send("hello there!")

    # if the message doesnt start with the command and the user is allowed
    ## for now, I will keep out the /arc_ check
    if message.author.id in reaction_enabled_users:
      emojis = self.reactions.get(message.channel.id, self.default_reactions)
      for emoji in emojis:
        await message.add_reaction(emoji)

  # --------------------------------------------------

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.user_id == self.bot.user.id:
      return
    

    # # Fetch the necessary information using the payload
    channel = self.bot.get_channel(payload.channel_id)
    if channel is None:
      channel = await self.bot.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)
    user = await self.bot.fetch_user(payload.user_id)
    emoji = payload.emoji

    # Now you have all the necessary objects to work with
    print(f"{user.name} reacted to message {message.id} with {payload.emoji}")

    # # Check if the reaction is the fire emoji
    if emoji.name == "🔥":
      await channel.send(f"{user.name} reacted with 🔥")
      await message.pin()

  # --------------------------------------------------

  @commands.command(name='react')
  async def react_option(self, ctx, option = None):
    if ctx.author == self.bot.user:
      return
    
    if option is None:
      await ctx.send("dude you have to tell me something here...")

    elif option == 'set':
      await ctx.send('react set command triggered!')
      message_content = ctx.message.content
      emojis = self.extract_emojis(message_content)
      self.reactions[ctx.channel.id] = emojis
      await ctx.send(f'Reactions updated for this channel: {emojis}')

    elif option == 'nope':
      await ctx.send('nope!')
      
    elif option == 'test':
      await ctx.send('test successful! probably')

  # --------------------------------------------------

  def extract_emojis(self, message_content):
    return ''.join(c for c in message_content if c in emoji.UNICODE_EMOJI)





def setup(bot):
  bot.add_cog(ReactBot(bot))