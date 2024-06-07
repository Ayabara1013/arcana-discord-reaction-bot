# import the necessary libraries from discord.py
import discord
from discord.ext import commands

# define the bot's intentions, specifying it should recieve message content
intents = discord.Intents.default()
intents.message_content = True

# initialize the bot with a command prefix and specified intents
bot = commands.bot(command_prefix = '!arc ', intents = intents)

# Dictionary to store the emojis for reactions
# The key will be the channel ID and the value will be a list of emojis
reactions = {}

#event handler for when the bot is ready
@bot.event
async def on_ready():
  print(f'Bot is ready. logged in as {bot.user}')

# event handler for when a message is sent in the channel
@bot.event
async def on_message(message):
  #ignore messages sent by the bot itself to prevent a loop
  if message.author == bot.user:
    return
  
  # if message.content.startswith('!arc react sort'):
  #   # show the stuff
  #   await ctx.send(f'current reaction order: {reactions[ctx.channel.id]}')

  #   # prompt for the new order
  #   await ctx.send(f'please enter new order:')

  #   # wait for the response
  #   try:
  #     order_message = await bot.wait_for('message', check=check, timeout=60)
  #     #parse the order
  #     emojis = order_message.content.split()
  #     # update the reactions library
  #     reactions[message.channel.id] = emojis

  #     await message.channel.send(f'Order updated: {emojis}')

  #   except TimeoutError:
  #     await message.channel.send("Timeout: No response received.")

  # if the channel has specified reactions, add them to the message
  if message.channel.id in reactions:
    for emoji in reactions[message.channel.id]:
      await message.add_reaction(emoji)

  # ensure other commands are processed
  await bot.process_commands(message)


# Command to add an emoji to the reaction list for the current channel
@bot.command(name = 'addemoji')
async def add_emoji(ctx, emoji):
  #if the channel is not in the reactions dictionary, add it
  if ctx.channel.id not in reactions:
    reactions[ctx.channel.id] = []

  #add the specified emoji to the channels reaction list
  reactions[ctx.channel.id].append(emoji)
  await ctx.send(f'Added {emoji} to reactions.')

# command to remove an emoji from the reaction list for the current channel
@bot.command(name='removeemoji')
async def remove_emoji(ctx, emoji):
  # check if the channel and emoji are in the reactions dictionary
  if ctx.channel.id in reactions and emoji in reactions[ctx.channel.id]:
    reactions[ctx.channel.id].remove(emoji)
    await ctx.send(f'Removed {emoji} from reactions.')
  else:
    await ctx.send(f'{emoji} not found in reactions.')



# Command to list the current emojis in the reaction list for the current channel
@bot.command(name='listemojis')
async def list_emojis(ctx):
    # Check if the channel has any reactions configured
    if ctx.channel.id in reactions:
        await ctx.send(f'Current emojis: {" ".join(reactions[ctx.channel.id])}')
    else:
        await ctx.send('No emojis configured for this channel.')





# @bot.command(name = 'sortemojis')
# async def sort_emoji():
#   newSet = []

#   for emoji in sortString:
#     if emoji not in reactionSet:
#       return
#     newSet.append(emoji)
  
#   print(f'new order is {newSet}')

#   reactionSet = newSet
#   return


# command comes in
# command is sort
# bot shows all the emojis FOR THAT CHANNEL and the order theyre in,
# some method to sort them?


# testLib = {
#   123: ['2️⃣', '3️⃣', '1️⃣', '4️⃣', '5️⃣']
# }

# # command to manually sort the list
# @bot.command(name='react sort')
# async def react_sort(ctx):
#   #retrive the list of emojis for the channel
#   emojis = [emoji for emoji in ctx.channel.guild.emoji if not emoji.animated]

#   # display the list of emojis
#   # await ctx.send(f'current order: {emojis}')

#   emoji_str = join(emojis)
#   await ctx.send(f'{emoji_str}')



#   # read the responses, and establish the new order
