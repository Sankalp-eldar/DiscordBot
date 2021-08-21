import discord
from discord.ext import commands
from modules import read_json,write_json

TOKEN = ""
bot_data_file = 'bot_data.json'



intents = discord.Intents.all()
# intents.members = True

client = commands.Bot(command_prefix=";;",help_command=None,
    intents=intents,case_insensitive=True)


# ____ Bot logged in and ready ___
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
        name="YOU, and Reading."))
    print(f"HI, wow {client.user}")

def data_reset():
    client.blacklisted_channels = dict()
    client.ignored_channels = dict()
    client.guild_moderator = dict()
    client.guild_activities = dict()
    client.guild_welcomes = dict()
    data = read_json(bot_data_file)
    client.bot_admins = data["bot_admins"]
    del data["bot_admins"]


    for ke,val in data.items():
        # for i in data[j]:
        if "blacklisted_channels" in val:
            # client.blacklisted_channels.extend(data[i]["blacklisted_channels"])
            client.blacklisted_channels[int(ke)] = data[ke]["blacklisted_channels"]
        if "moderator" in val:
            client.guild_moderator[int(ke)] = data[ke]["moderator"]
        if "activity" in val:
            client.guild_activities[int(ke)] = data[ke]['activity']
        if "welcome" in val:
            client.guild_welcomes[int(ke)] = data[ke]['welcome']
        if "ignored_channels" in val:
            client.ignored_channels[int(ke)] = data[ke]['ignored_channels']

data_reset()
 


# ______ Extension loders ______

@client.command(hidden=True)
async def load(ctx,extension):
    try:client.load_extension(f"extensions.{extension}")
    except Exception as e:
        print(e)
        await ctx.send("Error while loading.")
    else:
        await ctx.send("Loaded: {} successfully".format(extension))

@client.command(hidden=True)
async def unload(ctx,extension):
    try:client.unload_extension(f"extensions.{extension}")
    except Exception as e:
        print(e)
        await ctx.send("Error while Unloading.")
    else:
        await ctx.send("Unloaded: {} successfully".format(extension))

@client.command(hidden=True)
async def reload(ctx,extension):
    client.reload_extension(f"extensions.{extension}")
    await ctx.send("reloaded: {} successfully".format(extension))

@client.command(hidden=True)
async def refresh(ctx):
    if ctx.author.id not in client.bot_admins:return
    data_reset()
    if ctx.guild:
        await ctx.message.delete()
        await ctx.author.send("✅")
    else:
        await ctx.send("It's Done!")

# _ loders end _




# ___ coppied ___ # eval command
import contextlib
import io
import textwrap
from traceback import format_exception
from modules import clean_code, Pag


@client.command(name='eval',aliases=['py'],hidden=True)
async def _eval(ctx, *, code):
    if ctx.author.id not in client.bot_admins:	
      return
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
            if result == "\n-- None\n":
                return await ctx.message.add_reaction(emoji="✅")
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=100,
        entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```"
    )

    await pager.start(ctx)








# ____ Other commands ____



# __ guild join __
@client.event
async def on_guild_join(guild):
    data = read_json(bot_data_file)
    # if guild.id not in data:
    data[str(guild.id)] = {"name": guild.name,"moderator":[guild.owner_id],
    'blacklisted_channels':list(),"ignored_channels":list()}
    write_json(data,bot_data_file)
    client.blacklisted_channels[guild.id] = list()

@client.event
async def on_guild_remove(guild):
    data = read_json(bot_data_file)
    del data[str(guild.id)]
    write_json(data,bot_data_file)


# __ reading all messages __
@client.event
async def on_message(message):
    if message.author.id == 814185418945462342:return
    if message.guild:
        if await blacklists(message):return
        if message.content.startswith(";;"):
            if message.channel.id in client.ignored_channels[message.guild.id]\
            and message.author.id not in client.guild_moderator[message.guild.id]:
                return
            if await mod_commands(message):return

    await client.process_commands(message)


async def blacklists(message):
    guild = message.guild.id
    if message.channel.id in client.blacklisted_channels[guild] \
    and message.author.id not in client.guild_moderator[guild]:
        await message.delete()
        return True

mod_cmds_list = ['mod','blacklist','bl',"no","stop",
        'ban_channel','moderator']
async def mod_commands(message):
    guild = message.guild.id
    if True in [message.content.lower().strip(";;").startswith(i) for i in mod_cmds_list]:
        if message.author.id in client.bot_admins:return False
        if message.author.id not in client.guild_moderator[guild]:
            await message.delete()
            return True

# @client.event
# async def on_member_update(before,after):
#     guild = after.guild.id
#     # if before != after:
#     print(f"{before} , S:{before.status} , A:{before.activity}")
#     print(f"{after} , S:{after.status} , A:{after.activity}")
#     # ch = client.get_channel(825680959629426709)
#     # await ch.send(f"{after.name} , {after.status} , {after.activity} {after}")


# @client.event
# async def on_user_update(before,after):
#     guild = after.guild.id
#     print(f"upd: {after.name} , {after.status} , {after.activity} {after}")
    # ch = await client.get_channel(825680959629426709)
    # await ch.send(f"{after.name} , {after.status} , {after.activity} {after}")




@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.errors.CommandNotFound):
        return
    if isinstance(err, commands.errors.MissingPermissions):
        msg = await ctx.send(str(err))
        await msg.delete(delay=3)
        return
    if isinstance(err, commands.errors.MissingRequiredArgument):
        msg = await ctx.send("Incorrect syntax for command")
        await msg.delete(delay=3)
        return
    raise err



if __name__ == '__main__':
    # client.add_listener(reader, 'on_message')
    # client.add_listener(guild_join, "on_guild_join")

    client.load_extension("extensions.story")
    client.load_extension("extensions.utility")
    client.load_extension("extensions.management")
    client.load_extension("extensions.help")
    client.load_extension("extensions.misc")


    client.run(TOKEN)