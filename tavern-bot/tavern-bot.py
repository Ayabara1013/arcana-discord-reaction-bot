from discord.ext import commands

class TavernBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='createlorechannel')
    async def create_lore_channel(self, ctx, name: str = None):
        guild = ctx.guild

        try:
            if name:
                await guild.create_text_channel(name)
            else:
                await guild.create_text_channel(f"{ctx.channel.name}-lore")
            await ctx.send(f'Channel {"`" + name + "`" if name else "`" + ctx.channel.name + "-lore`"} created successfully!')
        except discord.Forbidden:
            await ctx.send('I do not have permission to create channels.')
        except discord.HTTPException as e:
            await ctx.send(f'An error occurred: {e}')

def setup(bot):
    bot.add_cog(TavernBot(bot))
