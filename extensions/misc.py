import discord
from discord.ext import commands
from modules import read_json,write_json
from PIL import Image, ImageDraw
from io import BytesIO
from typing import Union

img_ape = "images/Monkewithjungle.png"
# (455,302) pos,  resize (350,350)
# (915,630) pos, resize (700,700)

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


class Misc(commands.Cog):
    def __init__(self,client):
        self.client = client

    async def welcome_base(self,user,location=(0,0),size=None,_round=0):
        pfp = user.avatar_url_as()
        pfp = BytesIO(await pfp.read())

        pfp = Image.open(pfp)
        if isinstance(size,(tuple,list,set)):
            pfp = pfp.resize(size)

        with Image.open(img_ape) as im:
            im.paste(pfp, location )

            path = "/".join(img_ape.split("/")[:-1]) + f"/{user.guild.id}_{user.id}.png"
            im = add_corners(im,_round)
            im.save( path )
        return path

    @commands.command(name="welc")
    async def welcome_test(self,ctx,user : Union[discord.Member,str] = None,_round=False,
        channel :discord.TextChannel = None):
        if isinstance(user, (str,type(None)) ):
            user = ctx.author
            if user:
                _round = True

        path = await self.welcome_base(user,location=(43,199),size=(156,156), _round=_round)

        await ctx.send(file= discord.File(path))

    @commands.command(name="welcmsg",aliases=["welcome",'join'])
    @commands.has_permissions(administrator=True)
    async def welcmsg(self,ctx,send : discord.TextChannel,toggel="false"):
        guild = ctx.guild.id
        if toggel in [True,'t','enable','true']:
            data = read_json("bot_data.json")
            data[str(guild)]['welcome'] = send.id
            try:
                self.client.guild_welcomes[guild] = send.id
            except AttributeError:
                self.client.guild_welcomes = {guild:send.id}
            write_json(data,"bot_data.json")
            await ctx.message.delete()
            await ctx.send(f"New members will be welcomed in <#{send.id}>")
        else:
            data = read_json("bot_data.json")
            if data[str(guild)].get('welcome'):
                del data[str(guild)]['welcome']
                del self.client.guild_welcomes[guild]
                write_json(data, "bot_data.json")
                await ctx.message.delete()
                await ctx.send(f"Stopped User welcome.")

    @commands.Cog.listener(name="on_member_join")
    async def welcome(self,member):
        if member.bot:return
        guild = member.guild
        channel = self.client.guild_welcomes.get(guild.id)
        if not channel:return

        path = await self.welcome_base(member,location=(43,199),size=(156,156), _round=36)
        file = discord.File(path,filename=f"welcome.png")

        embed = discord.Embed(title=f"Welcome {member.name}!",
        description=f"HI! {member.name} Member #{guild.member_count}")
        embed.add_field(name=f"Welcome to {guild.name}.",value ="Apes together Strong!!!\n\nCheck <#803839036338864168> !!")

        embed.set_image(url="attachment://welcome.png")
        embed.set_footer(text=f"{member.joined_at.strftime('%d %b, %Y at %I:%M:%S %p')}")
        embed.set_thumbnail(url=guild.icon_url)

        channel = guild.get_channel(channel)
        await channel.send(file=file, embed=embed)

carl = {"title":"Welcome to {server}",
"description":"HI! {user(name)} Memember #{server(members)}\nWelcome the Server.\nApes together Strong!!!\n\nCheck <#803839036338864168> !!",
"thumbnail":{"url":"{server(icon) }"},
"image":{"url":"{user(icon)}"},
"color":3715769,
"footer":{"icon_url":"",
"text":"{user(joined_at) }"}}

me = {"fields":[
    {"name":"VERY IMPORTANT",
    "value":"Basic stats of server:\nbots: {server(bots) }\nI wonder how did my future self manage to get you here. ",
    "inline":"true"}
    ],
"title":"Welcome to {server}",
"description":"You are VERY new.\nWhy even are you here if you are not a bot?\nDo you want to get experimented upon.",
"thumbnail":{"url":"{server(icon) }"},
"image":{"url":"{user(icon)}"},
"author":{"name":"{server(owner) } Owner",
"url":"",
"icon_url":"https://cdn.discordapp.com/avatars/580009035743494156/9d48b999aa1cb6c7f603cd66d9be3611.webp?size=1024"},
"color":0,
"footer":{"icon_url":"https://cdn.discordapp.com/avatars/235148962103951360/cececd50fdc87b29929e65c768f24ad6.webp?size=1024",
"text":"Thanks to carl for welcome message.    {user(joined_at) }"}}


def setup(client):
    client.add_cog(Misc(client))