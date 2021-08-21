import discord
from discord.ext import commands

# ____ STORY ___
compile_help = discord.Embed(
    title=";;help compile",
    description="Combines all messages from given messageId to current message\
See `;;help start`",
    color=65535
    )
compile_help.add_field(name="Usage:",value="`;;compile <MessageID>`",inline=False)
compile_help.add_field(name="Aliases:",value="c",inline=False)
compile_help.set_footer(text="You need to turn on devloper mod to get message Id.")

start_help  = discord.Embed(
    title=";;help start",
    description="Marks the starting of a story.\nNow you dont have to give a messageID\
Use `;;end` to end a story.",
    color=65535
    )
start_help.add_field(name="Usage:",value="`;;start [text]`",inline=False)
start_help.add_field(name="Aliases:",value="sts",inline=False)
start_help.add_field(name="Delaits:",value="[text] will be sent to mark start of story\
It won't be included in story",inline=False)

end_help  = discord.Embed(
    title=";;help start",
    description="Marks the Ending of a story.\nSee `;;help start`.",
    color=65535
    )
end_help.add_field(name="Usage:",value="`;;end [send] [title]`",inline=False)
end_help.add_field(name="Aliases:",value="ss",inline=False)
end_help.add_field(name="Default value:",value="[title] : **CURRENT STORY**\
[send] : false",inline=False)
end_help.add_field(name="Delaits:",value="[title] will be used as heading of story\
[send] if true will send story in channel else DM the user.",inline=False)


# ____ UTILITY ____
echo_help = discord.Embed(
    title=";;help echo",
    description="sends text to mentioned channel",
    color=65535
    )
echo_help.add_field(name="Usage:",value="`;;echo <#channel | channelID> [text]`",inline=False)


purge_help = discord.Embed(
    title=";;help purge",
    description="Deletes the given number of messages starting from current message",
    color=65535
    )
purge_help.add_field(name="Usage:",value="`;;purge [number]`",inline=False)
purge_help.add_field(name="Aliases:",value="2, clean",inline=False)
purge_help.add_field(name="Default value:",value="2",inline=False)



# _____ management _____

mod_help = discord.Embed(
    title=";;help moderator",
    description="Add/Remove a Member as Bot manager of this server.",
    color=65535
    )
mod_help.add_field(name="Usage:",
    value="`;;moderator <add/a | remove/r> <@user | userID>`",inline=False)
mod_help.add_field(name="Aliases:",value="mod",inline=False)


ban_channel_help = discord.Embed(
    title=";;help ban_channel",
    description="Removes messages from all users in blacklisted channels\
    Except messages from bot moderator. (see `;;help mod` to add moderator)",
    color=65535
    )
ban_channel_help.add_field(name="Usage:",
    value="`;;ban_channel <#channel | channelID> [true | false]`",inline=False)
ban_channel_help.add_field(name="Aliases:",value="no, stop, ban",inline=False)
ban_channel_help.add_field(name="Enable ban aliases",value='true, yes, ban, t',inline=False)
ban_channel_help.add_field(name="Default value:",value="false",inline=False)



blacklist_help = discord.Embed(
    title=";;help blacklist",
    description="Shows blacklisted channels in the server.\
    (see `;;help ban_channel` to add channel to blacklist)",
    color=65535
    )
blacklist_help.add_field(name="Usage:",
    value="`;;blacklist`",inline=False)
blacklist_help.add_field(name="Aliases:",value="bl",inline=False)


modlist_help = discord.Embed(
    title=";;help blacklist",
    description="Shows Bot mannagers for this bot.",
    color=65535
    )
modlist_help.add_field(name="Usage:",
    value="`;;modlist`",inline=False)
modlist_help.add_field(name="Aliases:",value="ml",inline=False)

activity_help = discord.Embed(
    title=";;help tracklist",
    description="Shows Channel where user activity is send.",
    color=65535
    )
activity_help.add_field(name="Usage:",
    value="`;;tracklist`",inline=False)
activity_help.add_field(name="Aliases:",value="al, activitylist",inline=False)


help_all = discord.Embed(
    title='All commands',
    colour= 65535,
    description="run `;;help <command>` to know more about the command."
    )
help_all.add_field(name="Story*",value="`compile`\n`start`\n`end`",inline=False)
help_all.add_field(name="Utility",value="`purge`**\n`echo`",inline=False)
help_all.add_field(name="Management*",
    value="`moderator`\n`ban_channel`\n`blacklist`\n`modlist`\n`tracklist`",inline=False)

help_all.set_author(name="Help section")
help_all.add_field(name="Note",value="* commands require special permission (bot manager)\
\n** command require user to have admin permission")

img_help = discord.Embed(title="`;;img` Methods here:", description="`placexy`, `round`, `placepfp`")
img_help.add_field(name="placexy | xy",value="place image y over x. provide it messageID of attachment/image in order x,y\
    \n ex: `;;img placexy 872476602306233 88234870234760 [co-ordinate X of y] [co-ordinate Y of y]`\
    \nfirst ID is image over which second image would be placed.")

img_help.add_field(name="round",value="returns a image with round corners\
    \n`;;img round <Messsageid> [radins]` radins is default 100")

img_help.add_field(name="placepfp | pfp", value="returns pfp placed over image x\
    \n`;;img placepfp <Messsageid> <co-ordinate X> <co-ordinate Y> <pfp size>`\
    \nX-Y are pixle distance from top left, just like paint in windows\
    \n since pfp's in discord are square <pfp size> will be used as both width and height")




class help(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.group(name="help",invoke_without_command=True)
    async def help(self,cxt):
        await cxt.send(embed=help_all)



    @help.command(name='compile',aliases=['c'])
    async def compile_(self,cxt):
        await cxt.send(embed=compile_help)

    @help.command(name='start',aliases=['sts'])
    async def start(self,cxt):
        await cxt.send(embed=start_help)

    @help.command(name='end',aliases=['ss'])
    async def end(self,cxt):
        await cxt.send(embed=end_help)



    @help.command(name='echo')
    async def echo(self,cxt):
        await cxt.send(embed=echo_help)

    @help.command(name='purge',aliases=['2','clean'])
    async def purge(self,cxt):
        await cxt.send(embed=purge_help)



    @help.command(name='moderator',aliases=['mod'])
    async def moderator(self,cxt):
        await cxt.send(embed=mod_help)

    @help.command(name='ban_channel',aliases=['no','stop','ban'])
    async def remove_any(self,cxt):
        await cxt.send(embed=ban_channel_help)

    @help.command(name='blacklist',aliases=['bl'])
    async def blacklist(self,cxt):
        await cxt.send(embed=blacklist_help)

    @help.command(name='modlist',aliases=['ml'])
    async def modlist(self,cxt):
        await cxt.send(embed=modlist_help)

    @help.command(name='tracklist',aliases=['al','activitylist'])
    async def tracklist(self,cxt):
        await cxt.send(embed=activity_help)

    @help.command(name='img')
    async def img(self,cxt):
        await cxt.send(embed=img_help)

def setup(client):
    client.add_cog(help(client))