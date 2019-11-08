import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
from itertools import cycle
import time
import youtube_dl

my_token = 'NTE0MTcyNTQ0NzUzMDc0MTk2.DtSurw.FZAmiYJFMc5278T9shyzwPCySo8'

client = commands.Bot(command_prefix = '+')

client.remove_command('help')
status = ['+help for commands', 'With code', "something"]

players = {}


async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name =current_status))
        await asyncio.sleep(20)

@client.event
async def on_ready():
    print('The bot is online and is connected to discord')


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='members')
    await client.add_roles(member, role)


@client.event
async def on_message(message):
    
    await client.process_commands(message)
    if message.content.startswith('Sup dude'):
        userID = message.author.id
        await client.send_message(message.channel, '<@%s> sup' % (userID))

@client.command(pass_context =True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(Colour = discord.Colour.orange())
    embed.set_author(name = 'Help Commands')
    embed.add_field(name ='+say', value ='Returns what the user says.', inline=False)
    embed.add_field(name ='+clear', value ='Deletes certain amount of messages, default amount is 10', inline=False)
    embed.add_field(name ='+join', value ='The bot joins the current voice channel, the user must be in a voice channel to use this comand', inline=False)
    embed.add_field(name ='+leave', value ='The bot leaves the current voice channel.', inline=False)
    embed.add_field(name ='+play', value ='Plays the audio from a youtube url', inline=False)
    embed.add_field(name ='+serverinfo', value ='Gives the server information on the selected user', inline=False)
    embed.add_field(name ='Sup dude', value =' says sup XD', inline=False)

    await client.send_message(author, embed=embed)


@client.command(pass_context = True)
@commands.has_permissions(kick_members=True) 
async def clear(ctx, amount = 10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount) +1):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(str(amount) + ' messages were deleted')
    


@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    embed = discord.Embed(
        title = 'Voice channel',
        description = 'commands for the voice channel.',
        colour = discord.Colour.blue()
    )

    embed.add_field(name = '+play', value = 'play youtube audio with url', inline = False)
    embed.add_field(name = '+pause', value = 'pauses audio', inline = False)
    embed.add_field(name = '+resume', value = 'resumes audio', inline = False)
    embed.add_field(name = '+leave', value = 'leave voice channel', inline = False)

    await client.say(embed=embed)
    await client.join_voice_channel(channel)


@client.command(pass_context = True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context = True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@client.command(pass_context = True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context = True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context = True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()



@client.command()
@commands.has_permissions(manage_messages=True) 
async def say(*args):
        output = ''
        for word in args:
            output += word
            
            output += ' '

        await client.say(output)
        
        
        
           
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mod(ctx, user:discord.Member,):
    await client.delete_message(ctx.message)
    role = discord.utils.get(ctx.message.server.roles, name='MOD')
    await client.add_roles(ctx.message.mentions[0], role)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)     
async def makehelper(ctx, user: discord.Member):
    nickname = '[TH]' + user.name
    await client.change_nickname(user, nickname=nickname)
    role = discord.utils.get(ctx.message.server.roles, name='TRIAL-HELPER')
    await client.add_roles(user, role)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Congratulations Message')
    embed.add_field(name = '__Congratulations__',value ='**Congratulations for TRIAL HELPER.Hope you will be more active here. Thanks for your help and support.**',inline = False)
    embed.set_image(url = 'https://preview.ibb.co/i1izTz/ezgif_5_e20b665628.gif')
    await client.send_message(user,embed=embed)
    await client.delete_message(ctx.message)
    
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)     
async def removehelper(ctx, user: discord.Member):
    nickname = user.name
    await client.change_nickname(user, nickname=nickname)
    role = discord.utils.get(ctx.message.server.roles, name='TRIAL-HELPER')
    await client.remove_roles(user, role)
    await client.delete_message(ctx.message)

        
        
        
        
        
        
       
        
        
        
        

@client.command(pass_context=True)
async def serverinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)


client.loop.create_task(change_status())
client.run('NTE0MTcyNTQ0NzUzMDc0MTk2.DtSurw.FZAmiYJFMc5278T9shyzwPCySo8')
