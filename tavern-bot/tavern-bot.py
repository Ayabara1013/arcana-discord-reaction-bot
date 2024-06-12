
import discord
from discord.ext import commands
import emoji
import boto3
from botocore.exceptions import ClientError

library = {}

# assign a channel to be a game channel / assign tags
@bot.command(name = 'tagChannel')
async def tag_channel(ctx):
  channel.send('how do you want to tag this channel?')

  container = []

  container[0] = discord.ActionRow

  container[0][0] += discord.Button
  

  action_row = {
    button1: 'lore'
  }

# assign linked lore channel

## create linked channel if need be



# replicate / copy message to lore channel when tagged
## initially, just add it to the lore channel when tagged

# --------------------------------------------------

@bot.event
async def on_raw_reaction_add(payload):
  # Check if the reaction is added by the bot
  if payload.user_id == bot.user.id:
    return

  # Fetch the necessary information using the payload\
  guild = bot.get_guild(payload.guild_id)
  channel = await bot.fetch_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = await bot.fetch_user(payload.user_id)
  emoji = payload.emoji

  # target_channel = library.channels[channel].lore_channel
  target_channel_name = str(f'{channel.name}' + '-lore')
  target_channel = guild.channel.name.target_channel_name

  # Now you have all the necessary objects to work with
  print(f"{user.name} reacted to message {message.id} with {payload.emoji}")


  # Check if the reaction is the paperclip emoji
  if emoji.name == "📎":  # This is the paperclip emoji
    # Create a new text channel with the name of the current channel + '-lore'
    new_channel_name = f"{channel.name}-lore"
    await guild.create_text_channel(new_channel_name)
    await channel.send(f"you were missing a lore channel, so I created it for you: {new_channel_name}")



  if emoji.name =='📎':
    print(f'{user.name} is tagging a message')
    
    if user in target_channel.allowed_users:
      print(f'{user.name} is a valid user')

      # does the channel exist?
      if not message.guild.channels.target_channel:
        print(f'{target_channel_name} does not exist. creating channel...')
        await create_lore_channel(message, target_channel_name)

      await target_channel.send(f'{user.name}' + {date})
      await target_channel.send(f'> {message}')

    elif user not in target_channel.allowed_users:
      print(f'{user.name} is not a valid user for this tag. rejecting the command')

# --------------------------------------------------


## remove message from lore channel when tagged (in either location?)