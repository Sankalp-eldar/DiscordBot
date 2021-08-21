import discord, asyncio, os
from discord.ext import commands
# from modules import read_json,write_json
from PIL import Image, ImageDraw
from io import BytesIO
from functools import partial
# from typing import Union


img_path = "images"
img_help_is_here = img_path + "/dont-worry-help.png"
img_here_to_help = img_path + "/i-am-here-to-help-you.png"
img_help_is = img_path + "/help_is.png"
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


class Image_Manu(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command(name="send")
    async def send_(self,ctx,mode="help",*, talk=None):
        if ctx.message.mentions:
            target = ctx.message.mentions[0]
        else:
            target = ctx.author

        img = target.avatar_url_as()
        img = BytesIO(await img.read())

        if mode == 'help':
            bg = img_help_is_here
            posx,posy = 114, 59
            size = (140,140)
            # img = Image.open(img).convert("RGB")
            # img = img.resize((140,140))
            # img = add_corners(img, 180)
        elif mode == 'helper':
            bg = img_here_to_help
            posx,posy = 10, 106
            size = 141,141
        elif mode == '..':
            bg = img_help_is
            posx,posy = 0,0
            size = 1,1

        path = await self.pool_func(self.user_paste, user=target, bg=bg, img=img, location=(posx,posy),size=size)

        await ctx.send(file = discord.File(path,filename=f"send{path[-4:]}"))

        await self.pool_func(os.remove, path=path)


    def user_paste(self, user, bg, img, location, size=None,rad=100,_round=False):

        if not isinstance(img,Image.Image):
            pfp = Image.open(img)
        else:
            pfp = img
        if size:
            pfp = pfp.resize(size) 

        path = img_path + f"/{user.guild.id}_{user.id}.png"
        with Image.open(bg) as im:
            im.paste(pfp, location )
            if _round in ['t','true',True,'round']:
                im = add_corners(im,rad)
            im.save( path )

        return path

    async def pool_func(self,func,**kw):
        loop = asyncio.get_running_loop()
        func = partial(func,**kw)
        result = await loop.run_in_executor(None, func)
        return result

    @commands.group(name="img",invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def img(self,ctx,*,val=None):
        emb = discord.Embed(title="Methods here:", description="`placexy`, `round`, `placepfp`")
        emb.add_field(name="placexy | xy",value="place image y over x. provide it messageID of attachment/image in order x,y\
            \n ex: `;;img placexy 872476602306233 88234870234760 [co-ordinate X of y] [co-ordinate Y of y]`\
            \nfirst ID is image over which second image would be placed.")

        emb.add_field(name="round",value="returns a image with round corners\
            \n`;;img round <Messsageid> [radins]` radins is default 100")

        emb.add_field(name="placepfp | pfp", value="returns pfp placed over image x\
            \n`;;img placepfp <Messsageid> <co-ordinate X> <co-ordinate Y> <pfp size>`\
            \nX-Y are pixle distance from top left, just like paint in windows\
            \n since pfp's in discord are square <pfp size> will be used as both width and height")

        await ctx.send(embed=emb)

    @img.command(name="placexy",aliases=["xy"])
    @commands.has_permissions(administrator=True)
    async def placexy(self,ctx,x: discord.Message,y: discord.Message, posx:int=0, posy:int=0,*,talk=None):
        
        bg = x.attachments[0]
        bg = BytesIO(await bg.read())

        img = y.attachments[0]
        img = BytesIO(await img.read())

        path = await self.pool_func(self.user_paste, user=ctx.author, bg=bg, img=img, location=(posx,posy))
        # user_paste(self, user, bg, img, location, size=None,rad=100,_round=False)
        await ctx.reply(file = discord.File(path,filename=f"placexy{path[-4:]}"))

        await self.pool_func(os.remove, path=path)

    @img.command(name="placepfp",aliases=["pfp"])
    @commands.has_permissions(administrator=True)
    async def placepfp(self,ctx, bg: discord.Message, x :int, y :int, size:int, *, talk=None):

        bg = bg.attachments[0]
        bg = BytesIO(await bg.read())

        img = ctx.author.avatar_url_as()
        img = BytesIO(await img.read())

        # path = await self.user_paste(ctx.user, bg, img, (x,y), (size,size),rad=100,_round=talk)
        path = await self.pool_func(self.user_paste, user=ctx.author, bg=bg, img=img, location=(x,y),
            size=(size,size),rad=100,_round=talk)

        await ctx.reply(file = discord.File(path,filename=f"placepfp{path[-4:]}"))

        await self.pool_func(os.remove, path=path)

    @img.command(name="round")
    @commands.has_permissions(administrator=True)
    async def round_(self,ctx, msg : discord.Message,rad=100,*, talk=None):
        bg = msg.attachments[0]
        bg = BytesIO(await bg.read())

        with Image.open(bg) as im:
            im = add_corners(im, rad)
            path = img_path + f"/{ctx.guild.id}_{ctx.author.id}.png"
            await self.pool_func(im.save, fp=path)

        file = discord.File(path,filename=f"round{path[-4:]}")
        await ctx.reply(file = file)

        await self.pool_func(os.remove, path=path)


def setup(client):
    client.add_cog(Image_Manu(client))