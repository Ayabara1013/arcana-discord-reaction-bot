import discord
from discord.ext import commands
import boto3
from botocore.exceptions import ClientError
import asyncio

bot_command_prefix = "/arc "

print("\nStarting Arcana Bot...\n")

# --------------------------------------------------

# Define the bot's intentions, specifying it should receive message content
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# Initialize the bot with a command prefix and specified intents
bot = commands.Bot(command_prefix=bot_command_prefix, intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. logged in as {bot.user}\n')

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
    
    await ctx.channel.send('test successful from arcana-bot.py')

# Load the cog (extension)
async def load_extensions():
    initial_extensions = ['cogs.react-bot', 'cogs.test-bot']  # Note: 'cogs.test-bot' added to the module path
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}. Error: {type(e).__name__} - {e}')

# Asynchronous main function to run the bot
async def main():
    await load_extensions()
    await bot.start(bot_token)

# Run the bot using asyncio.run (Python 3.7+)
if __name__ == '__main__':
    asyncio.run(main())
