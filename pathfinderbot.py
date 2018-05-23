#!/usr/bin/env python3
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
Modified by Pathfinders
'''

import os
import json
import random
import aiohttp
import discord
from discord.ext import commands
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from aiohttp import web


description = '''Based on an example bot to showcase the discord.ext.commands
extension module, by Rapptz

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!', description=description)

### Use this function to get text (HTML) from URLs asynchronously ###
# async def get_page(url):
#     """
#     Accepts a URL.
#     Asynchronously retrieves a page from URL and returns it.
#     """
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#            return await resp.text()

### Use this function to get text (HTML) from URLs asynchronously ###
async def get_page(url):
    """
    Accepts a URL.
    Asynchronously retrieves a page from URL and returns it.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
        
### Use this function to get a raw response from URLs asynchronously ###
async def get_json(url):
    """
    Accepts a URL.
    Asynchronously retrieves a JSON response from URL and returns it.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return web.json_response(resp)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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
    # Appears to be broken.
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
    """Plays Rock Paper Scissors with the bot."""
    # Change user input to full lenght string for to say back later when telling who won
    if message.lower() == 'r':
        player_choice = 'rock'
    elif message.lower() == 'p':
        player_choice = "paper"
    elif message.lower() == 's':
        player_choice = 'scissors'
    else:
        await bot.say('Please try again using "!rps" + "r" or "p" or "s" to pick your play')
        return

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
            
    if player_choice == bot_choice:
        await bot.say('Your {} draws with my {}.'.format(player_choice, bot_choice))
 
@bot.command()
async def random_module():
    """Links to a random Python 3 module from the standard library."""
    my_url = 'https://docs.python.org/3/py-modindex.html'
    #get page, get soup
    page_html = await get_page(my_url)
    page_soup = soup(page_html, 'html.parser')

    containers = page_soup.find_all("td")
    module_list = []

    for container in containers:
        # check if text contained
        if container.text != '':
            #check if there is a link present
            if container.a != None:
                # print(container.text)
                # print(container.a['href'])
                module_list.append((container.text.strip(), container.a['href']))

    selected_module = (random.choice(module_list))
    url_base = 'https://docs.python.org/3/'

    await bot.say('You should do some reading about:\n {} , \nClick this link to read more: \n \
        {}{}'.format(selected_module[0], url_base, selected_module[1]))

@bot.command()
# command to get the first definition of a word using the Oxford English Dictionary API
# TODO - currently just gets the first definition, would like it to return them all.
async def definition(*, message: str):
    """Displays the first definition for a word according to oxforddictionaries.com."""
    try:
        app_id = oxford_id
        app_key = oxford_key
        base_url = 'https://od-api.oxforddictionaries.com/api/v1/entries/'

        language = 'en'
        word_id = message

        url = base_url + language + '/' + word_id.lower()
        print('about to make request')
        # json_data = await get_page(url, headers = {'app_id': app_id, 'app_key': app_key}).json()
        async with get_page(url, headers = {'app_id': app_id, 'app_key': app_key}).json() as json_data:
        # for printing info
        # r = await get_page(url, headers = {'app_id': app_id, 'app_key': app_key})
        # print("****code {}\n".format(r.status_code))
        # print("****text \n" + r.text)
        # print("****json \n" + json.dumps(r.json()))

        # Some kind of loop needed here to get all definitions insead of just the first one
            definitions = json_data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        
            await bot.say('The first definition of ' + message + ' I have is :\n' + definitions)
    except:
        # If it cant find the word
        await bot.say('Are you sure thats a word in the dictionary?')

@bot.command()
async def coin(*, message: str):
    """
    Coin command is returning the price from a specific coin in USD.
    """
    r = await get_page('https://min-api.cryptocompare.com/data/price?fsym=' + message.upper() + '&tsyms=USD')
    ### changed to account for async page loading
    # my_data = r.json()
    my_data = json.loads(r)
    for k, v in my_data.items():
        if str(v) == 'Error':
            await bot.say(f"{message.upper()} coin doesn't exists.")
            break
        await bot.say(f"{message.upper()} price is {str(v)} {k.upper()}.")

@bot.command()
async def pydoc(*, message: str):
    """
    Post a link to the python doc page for the requested module in chat.
    """
    page = await get_page('https://docs.python.org/3/py-modindex.html')
    page_soup = soup(page, 'lxml')
    base_url = 'https://docs.python.org/3/library/'
    # Check that requested module name is valid.
    mod_list = [mod.text for mod in page_soup.findAll('code')]
    if str(message) in mod_list:
        doc_link = base_url + message
        await bot.say(doc_link)
    else:
        await bot.say('"{}" does not appear to be a module in the standard library.'.format(message))
        return


# Run Bot
#### non-heroku method of loading keys
with open('oxford_dictionary_api.txt', 'r') as oxford_key_file:
    oxford_id = oxford_key_file.readline().rstrip()
    oxford_key = oxford_key_file.readline().rstrip()
with open('token.txt', 'r') as token_file:
    token = token_file.readline().rstrip()

#### Heroku method
# token = os.environ['TOKEN']
# oxford_id = os.environ['OXFORD_ID']
# oxford_key = os.environ['OXFORD_KEY']

bot.run(token)
