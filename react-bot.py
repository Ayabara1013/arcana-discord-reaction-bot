# import the necessary libraries from discord.py
import discord
from discord.ext import commands

import emoji

# define the bot's intentions, specifying it should recieve message content
intents = discord.Intents.default()
intents.message_content = True

# initialize the bot with a command prefix and specified intents
bot = commands.Bot(command_prefix='!arc ', intents=intents)

# Dictionary to store the default emojis for reactions
# The key will be the emoji set name and the value will be a list of emojis
default_reactions = ["🔥", "1️⃣", "2️⃣", "3️⃣", "4️⃣"]

# Dictionary to store the emojis for reactions in each channel
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
  
  # Check if the channel has specified reactions, otherwise use default
  emojis = reactions.get(message.channel.id, default_reactions)

  # Add emojis to the message
  for emoji in emojis:
    await message.add_reaction(emoji)

  # Ensure other commands are processed
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




@bot.command(name='react set')
async def react_set(ctx):
  #ensure message is not from bot
  if ctx.author == bot.user:
    return
  
  # get message content
  message_content = ctx.message.content

  #extract emojis from the message content
  emojis = extract_emojis(message_content)

  #update reactions dictionary with new emojis for the channel
  reactions[ctx.channel.id] = emojis
  
  #send confirmation message
  await ctx.send(f'Reactions updated for this channel: {emojis}')



# helper function to extract emojis
def extract_emojis(message_content):
  return ''.join(c for c in message_content if c in emoji.UNICODE_EMOJI)