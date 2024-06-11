



## listen for the reactions


## set managed channels
library = {}

@bot.command(name = 'managechannels')
async def manage_channels(arg1):
  if arg1 == "linklore":
    await channel.send('which channel will contain the story?')

    channel_target = get_channel_target()

    if not channel.name(channel_target):
      create_channel(channel_target)
    else:
      library.channel.lore_target = channel_target

  elif arg1 == 'turnsenabled':
    library.channel.turns: True
  elif arg1 == 'turnsdisabled':
    library.channel.turns: False

  

    # library = { 
    #   'rough-riders': { 
    #     id: 001234,
    #     lore_target: 'rough-riders-story',
    #     turns: True, 
    #     active_turn: player00233
    #   } 
    # }

## create alias canon channels
@bot.command(name = 'createlorechannel')
async def create_lore_channel(message, name):
  if not guild.channel:
    
    if name:
      await guild.create_text_channel(name)
    else: 
      await guild.create_text_channel(str(message.channel) + '-lore')
  


## set turn

@bot.command(name = 'setturn')
async def set_turn(player):
  if library.channel.active_turn == player:
    channel.send('that player is already active')
    return
  
  library.channel.active_turn = player

  