import discord,inspect
from discord.ext import commands
from modules import read_json,write_json

class Utility(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.command()
    async def echo(self,ctx,_id : discord.TextChannel,*,txt=None):
        if txt:
            perm = _id.permissions_for(ctx.author)
            if not perm.send_messages:
                return await ctx.message.add_reaction(emoji="❌")
            await _id.send(txt)
            await ctx.message.add_reaction(emoji="✅")

    @commands.command(aliases=["clean","2"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self,cxt,limit=2):

        await cxt.channel.purge(limit=limit)
        data = await cxt.send("Deleted {} messages.".format(limit))
        await data.delete(delay=1)

    @commands.command(name=".-",aliases=["botpurge","bc"],hiden=True)
    @commands.has_permissions(manage_messages=True)
    async def botdelete(self,cxt,limit=20):
        await cxt.message.delete()
        async for i in cxt.channel.history(limit=limit):
            if i.author.bot:
                await i.delete()
        msg = await cxt.send("Removed bot messages")
        await msg.delete(delay=3)

    @commands.command(name="..",aliases=["cls",'mymsg'])
    @commands.has_permissions(manage_messages=True)
    async def deleteme(self,cxt,limit=10):
        await cxt.message.delete()
        for i in await cxt.channel.history(limit=limit).flatten():
            if i.author.id == 814185418945462342:
                await i.delete()
            elif i.content.startswith(";;"):
                await i.delete()

    @commands.command(name="ClearDm",aliases=["cdm"])
    async def clear_dm(self,ctx,limit=20):
        if ctx.guild:
            return await ctx.author.send("It is for here.")
        async for i in ctx.channel.history(limit=limit):
            if i.author.id == 814185418945462342:
                await i.delete()


    @commands.command(name='track',aliases=['activity'])
    @commands.has_permissions(manage_messages=True)
    async def track(self,ctx,send : discord.TextChannel,toggel="false"):
      guild = ctx.guild.id
      if toggel in [True,'t','enable','true']:
        data = read_json("bot_data.json")
        data[str(guild)]['activity'] = send.id
        try:
          self.client.guild_activities[guild] = send.id
        except AttributeError:
          self.client.guild_activities = {guild:send.id}
        write_json(data,"bot_data.json")
        await ctx.message.delete()
        await ctx.send(f"Started Watching User Activity, Displaying at <#{send.id}>")
      else:
        data = read_json("bot_data.json")
        if data[str(guild)].get('activity'):
          del data[str(guild)]['activity']
          del self.client.guild_activities[guild]
          write_json(data, "bot_data.json")
          await ctx.message.delete()
          await ctx.send(f"Stopped Watching User Activity.")

    @commands.Cog.listener(name="on_member_update")
    async def tracking(self,before, after):
        if after.bot:return
        guild = after.guild.id
        channel = self.client.guild_activities.get(guild)
        if channel:
            if after.status != discord.Status.online:return
            bec = discord.utils.find(lambda x: isinstance(x, (discord.Activity,
                discord.Game,discord.Streaming)) ,before.activities)
            act = discord.utils.find(lambda x: isinstance(x, (discord.Activity,
                discord.Game,discord.Streaming)), after.activities)
        # if before.activity != after.activity:
            if None in {bec, act}:
                if isinstance(act,discord.Streaming):
                    channel = after.guild.get_channel(channel)
                    await channel.send(f"**{after.display_name}** is streaming **{act.game}** on **{act.platform}**\nWatch them here:{act.url}")
                elif isinstance(act,(discord.Game,discord.Activity)):
                    channel = after.guild.get_channel(channel)
                    await channel.send(f"**{after.display_name}** has started playing **{act.name}**")

                elif isinstance(bec,discord.Streaming):
                    channel = after.guild.get_channel(channel)
                    await channel.send(f"**{after.display_name}** has stopped streaming **{bec.game}**")
                elif isinstance(bec,(discord.Game,discord.Activity)):
                    channel = after.guild.get_channel(channel)
                    await channel.send(f"**{after.display_name}** has stopped playing **{bec.name}**")

    @commands.command(name="verify")
    async def verify(self, ctx):
        channel = ctx.channel
        if channel.id != 837915404675710986:
            return #await ctx.send("Why. why try to misuse this little bot.")
        user = ctx.author
        try:
            mem_role = ctx.guild.get_role(729299970590769195)
            await user.add_roles(mem_role, reason="Verified!")
        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(Utility(client))