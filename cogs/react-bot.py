import discord
from discord.ext import commands
import emoji



midjourney_bot_id = 936929561302675456
arcana_react_bot_id = 1248848353106726974

reaction_blocked_users = [arcana_react_bot_id]
reaction_enabled_users = {midjourney_bot_id}

print('react-bot loaded')

class ReactBot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.default_reactions = ["🔥", "1️⃣", "2️⃣", "3️⃣", "4️⃣"]
    self.reactions = {}
    self.pin_reaction = "🔥"

  # --------------------------------------------------

  @commands.Cog.listener()
  async def on_message(self, message):
    # print('a message was sent')

    #ignore messages sent by the bot itself to prevent a loop
    if message.author == self.bot.user:
      return
    
    # Check if the message content is "hi" (case-insensitive)
    if message.content.lower() == "react":
      await message.channel.send("success!")

    # if the message doesnt start with the command and the user is allowed
    ## for now, I will keep out the /arc_ check
    if message.author.id in reaction_enabled_users:
      emojis = self.reactions.get(message.channel.id, self.default_reactions)
      for emoji in emojis:
        await message.add_reaction(emoji)

    # # Process other commands or messages
    # await self.bot.process_commands(message)

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

    # ## if message.reactions == default_reactions: 
    # # # Check if the reaction is the fire emoji
    # if emoji.name == "🔥":
    #   await channel.send(f"{user.name} reacted with 🔥")
    #   await message.pin()

    if emoji.name == self.pin_reaction:
      # get the emojis tha should be on this message (channel-specific or default)
      expected_emojis = self.reactions.get(message.channel.id, self.default_reactions)

      # get all current reaction emojis on the message
      current_reaction_emojis = [str(reaction.emoji) for reaction in message.reactions]

      # check if the message has all the expected emojis
      has_all_emojis = all(emoji in current_reaction_emojis for emoji in expected_emojis)

      if has_all_emojis:
        await channel.send(f"{user.name} reacted with {self.pin_reaction}")
        await message.pin()
      else:
        print(f"Message {message.id} doesn't have all required emojis yet. Current: {current_reaction_emojis}, Expected: {expected_emojis}")


        
  # --------------------------------------------------

  @commands.command(name='react', pass_context = True)
  async def react_option(self, ctx, option):
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

  # --------------------------------------------------

  @commands.command(name='list')
  async def list_emojis(self, ctx):
    # Check if the channel has any reactions configured
    if ctx.channel.id in self.reactions:
      await ctx.send(f'Current emojis: {" ".join(self.reactions[ctx.channel.id])}')
    else:
      await ctx.send('No emojis configured for this channel.')

  # --------------------------------------------------


  @commands.command(name='test3')
  async def on_test(self, ctx):
    print('performing test3 on cogs.react-bot.py')

    #ignore messages sent by the bot itself to prevent a loop
    if ctx.author == self.bot.user:
      return
    
    await ctx.channel.send('test successful from react-bot.py')

async def setup(bot):
  await bot.add_cog(ReactBot(bot))