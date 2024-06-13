import discord
from discord.ext import commands
import boto3
from botocore.exceptions import ClientError
import asyncio

bot_command_prefix = "/arc "

print("\nStarting Arcana Bot...\n")

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
    return json.loads(secret)["bot_token"]

# Get the bot token from AWS Secrets Manager
bot_token = get_secret()


# Print the bot token
print("Bot Token:", bot_token, "\n")

# --------------------------------------------------

# define the bot's intentions, specifying it should recieve message content
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True


# initialize the bot with a command prefix and specified intents
bot = commands.Bot(command_prefix=bot_command_prefix, intents=intents)


#event handler for when the bot is ready
@bot.event
async def on_ready():
  print(f'Bot is ready. logged in as {bot.user}\n')
  await load_extensions()

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  
  if message.content.lower() == "hi":
    await message.channel.send("hello there!")

  # Process other commands or messages
  await bot.process_commands(message)




@bot.command(name='test1')
async def bot_test(ctx):
	if ctx.author == bot.user:
		return
	
	print('performing test1 on arcana-bot.py')
	await ctx.channel.send('test successful from arcana-bot.py\n')



# test all the things
@bot.command(name='testall')
async def test_all_tests(ctx):
	#execute the commands from the different cogs
	await ctx.invoke(bot.get_command('test1'))
	await ctx.invoke(bot.get_command('test2'))
	await ctx.invoke(bot.get_command('test3'))





# Load the cog (extension)
async def load_extensions():
	print(f'loading extensions...\n')

	initial_extensions = [
			'cogs.react-bot', 
			'cogs.test-bot'
	]  # Note: 'cogs.test-bot' added to the module path
	for extension in initial_extensions:
		try:
			await bot.load_extension(extension)
			print(f'Loaded extension: {extension}\n')
		except Exception as e:
			print(f'Failed to load extension {extension}. Error: {type(e).__name__} - {e}\n')

# Asynchronous main function to run the bot
async def main():
	await load_extensions()
	await bot.start(bot_token)

# Run the bot using asyncio.run (Python 3.7+)
if __name__ == '__main__':
	asyncio.run(main())