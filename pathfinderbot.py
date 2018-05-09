#/usr/bin/env python3
'''
-------------------------
The MIT License (MIT)

Copyright (c) 2015-2016 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
-------------------------
Modified by ΨNAK
'''

import discord
from discord.ext import commands
import random

# TODO: bot admin list and admin commands such as reloading of files

description = '''Based on an example bot to showcase the discord.ext.commands
extension module, by Rapptz

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def rmtest(ctx):
    """Deletes test commands from the "bot-testing" channel."""
    # TODO: check if bot has proper permissions
    garbage = list()
    testchan = 'bot-testing'
    if ctx.message.channel.name != testchan:
        await bot.say('That command can only be used in #bot-testing')
        return
    async for msg in bot.logs_from(ctx.message.channel):
        if msg.content in ['!test', '!rmtest']:
            print('BOT IS DELETING MESSAGE(S) as requested by {}'.format(
                ctx.message.author))
            garbage.append(msg)
    await bot.delete_messages(garbage)


@bot.command()
async def test():
    """Generic test function. May only output to terminal, rather than Discord.
    """
    for chan in bot.get_all_channels():
        print(chan)
    for mem in bot.get_all_members():
        print(mem)
    # print(bot.get_user_info())


@bot.command()
async def ping():
    """Responds with "Pong!\""""
    await bot.say('Pong!')

@bot.command()
async def pathfinders():
    """Info about the Pathfinders group."""
    with open('missive.txt') as info:
        for line in info.readlines():
            await bot.say(line)
    return

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    if times < 10:
        for _ in range(times):
            await bot.say(content)
    else:
        await bot.say("Really? Don't you think that's a little excessive?")

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.event
async def on_member_join(member):
    """Welcomes a new member to the server and provides introductory info."""
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await bot.send_message(server, fmt.format(member, server))
    # Should be cleaned up and made to be one bot.say() call
    welcome = [
        'Welcome to the server, {0.name}.'.format(member),
        'This is a learning environment. Please do not be afraid to ask ' +
        'questions in the general channel. Others may benefit from your ' +
        'question as well.',
        'Please take a moment to tell us which subjects you are focusing ' +
        'on learning, and which subjects you have experience with. ' +
        'This is so appropriate "roles" (labels) can be applied to you. ' +
        'Examples: Programmer, PHP, WebDesign, HTML5, LinuxAdmin, IT Security'
    ]
    for line in welcome:
        await bot.say(line)

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

@bot.command()
async def rps(*, message: str):
    # Change user input to full lenght string for to say back later when telling who won
    if message.lower() == 'r':
        player_choice = 'rock'
    elif message.lower() == 'p':
        player_choice = "paper"
    elif message.lower() == 's':
        player_choice = 'scissors'
    else:
        await bot.say('Please try again using "!rps" + "r" or "p" or "s" to pick your play')

    # print("player: ", player_choice)

    # Get a random selection for the bots choice
    selection = [
    'rock',
    'paper',
    'scissors']
    bot_choice = random.choice(selection)
    # print("bot: ", bot_choice)

    # Game logic:
    # 3x if/elif for the players 3 possible inputs
    # 2x if/elifs inside these to check if there is a win or loss in that game
    # else catches if there is a draw
    # TODO - lots of repetition in this section, could win/loss be decided by a function??
    if player_choice == 'rock':
        if bot_choice == 'scissors':
            await bot.say('Your {} beats my {}! YOU WIN'.format(player_choice, bot_choice))     
        elif bot_choice == 'paper':
            await bot.say('My {} beats your {}! YOU LOSE'.format(bot_choice, player_choice))
            
    elif player_choice == 'paper':
        if bot_choice == 'rock':
            await bot.say('Your {} beats my {}! YOU WIN'.format(player_choice, bot_choice))    
        elif bot_choice == 'scissors':
            await bot.say('My {} beats your {}! YOU LOSE'.format(bot_choice, player_choice))
    
    elif player_choice == 'scissors':
        if bot_choice == 'paper':
            await bot.say('Your {} beats my {}! YOU WIN'.format(player_choice, bot_choice))
            
        elif bot_choice == 'rock':
            await bot.say('My {} beats your {} ! YOU LOSE'.format(bot_choice, player_choice))
            
    else:
     # player_choice == bot_choice:
        await bot.say('Your {} draws with my {}.'.format(player_choice, bot_choice))
 


# Run Bot
with open('token.txt') as token_file:
    token = token_file.readline().rstrip()
bot.run(token)
