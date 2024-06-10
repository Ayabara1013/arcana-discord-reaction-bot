# import the necessary libraries from discord.py
import discord
from discord.ext import commands
import emoji
import boto3
from botocore.exceptions import ClientError


## ----- stuffs -----

# allowed target users
# allowed_target_users = [936929561302675456]
midjourney_bot_id = 936929561302675456


# stuff for the secret? amazon gave it to me
def get_secret():

    secret_name = "arcana-reaction-bot-token"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret



# Get the bot token from AWS Secrets Manager
bot_token = get_secret()

# Print the bot token
print("Bot Token:", bot_token)


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

#event handler for when a message is sent in the channel
@bot.event
async def on_message(message):
  #ignore messages sent by the bot itself to prevent a loop
  if message.author == bot.user:
    return
  
  elif message.author == midjourney_bot_id:
    # Check if the channel has specified reactions, otherwise use default
    emojis = reactions.get(message.channel.id, default_reactions)
    ###### INSTEAD add the defaults TO thechannel!

    # Add emojis to the message
    for emoji in emojis:
      await message.add_reaction(emoji)
  

  # Ensure other commands are processed
  await bot.process_commands(message)


# say hi
@bot.command(name = 'sayhi')
async def say_hi(ctx):
  await ctx.channel.send('hi!')


# Command to add an emoji to the reaction list for the current channel
@bot.command(name = 'add')
async def add_emoji(ctx, emoji):
  #if the channel is not in the reactions dictionary, add it
  if ctx.channel.id not in reactions:
    reactions[ctx.channel.id] = []

  #add the specified emoji to the channels reaction list
  reactions[ctx.channel.id].append(emoji)
  await ctx.send(f'Added {emoji} to reactions.')



# command to remove an emoji from the reaction list for the current channel
@bot.command(name='remove')
async def remove_emoji(ctx, emoji):
  # check if the channel and emoji are in the reactions dictionary
  if ctx.channel.id in reactions and emoji in reactions[ctx.channel.id]:
    reactions[ctx.channel.id].remove(emoji)
    await ctx.send(f'Removed {emoji} from reactions.')
  else:
    await ctx.send(f'{emoji} not found in reactions.')



# Command to list the current emojis in the reaction list for the current channel
@bot.command(name='list')
async def list_emojis(ctx):
    # Check if the channel has any reactions configured
    if ctx.channel.id in reactions:
        await ctx.send(f'Current emojis: {" ".join(reactions[ctx.channel.id])}')
    else:
        await ctx.send('No emojis configured for this channel.')




@bot.command(name='reactset')
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


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run(bot_token)
