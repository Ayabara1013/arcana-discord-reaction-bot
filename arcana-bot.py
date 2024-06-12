import discord
from discord.ext import commands
import asyncio
import boto3
from botocore.exceptions import ClientError
import os

bot_command_prefix = "/arc "

# --------------------------------------------------

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

# --------------------------------------------------

# define the bot's intentions, specifying it should recieve message content
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True


# initialize the bot with a command prefix and specified intents
bot = commands.Bot(command_prefix='/arc ', intents=intents)


#event handler for when the bot is ready
@bot.event
async def on_ready():
  print(f'Bot is ready. logged in as {bot.user}')

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  if message.content.lower() == "hi":
    await message.channel.send("hello there!")

  # Process other commands or messages
  await bot.process_commands(message)



@bot.command(name='test')
async def bot_test(message):
  if message.author == bot.user:
    return
  
  await message.channel.send('test successful from arcana-bot.py')


# load cogs
initial_extensions = [
  'react-bot.react-bot',
  # 'tavern-bot.tavern_bot'
]

bot.load_extensions('react-bot.react-bot')

# if __name__ == '__main__':
#   for extension in initial_extensions:
#     client.load_extension(extension)


# Run the bot
bot.run(bot_token)