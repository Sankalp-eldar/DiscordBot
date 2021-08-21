import discord
from discord.ext import commands

from modules import read_json,write_json



class Management(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.group(name="moderator",aliases=["mod"],invoke_without_command=True)
    async def add_mod(self,cxt):
        if (cxt.message.content.split()[0]) not in ["add", "remove",'a',"r"]:
            await cxt.send("Incorrect syntax.")


    @add_mod.command(name="add",aliases=['a'])
    async def add_(self, cxt,mod : discord.Member):
        guild = cxt.guild.id
        if mod.id not in self.client.guild_moderator[guild]:
            self.client.guild_moderator[guild].append(mod.id)

        data = read_json("bot_data.json")
        data[str(guild)]['moderator'] = self.client.guild_moderator[guild]
        write_json(data,"bot_data.json")

        await cxt.send(f"Added {mod.name} as moderator")
        await cxt.message.delete()



    @add_mod.command(name="remove",aliases=['r'])
    async def remove_(self, cxt,mod : discord.Member):
        guild = cxt.guild.id
        if mod.id not in self.client.guild_moderator[guild] \
        or mod.id == cxt.guild.owner_id:
            await cxt.message.delete()
            return

        self.client.guild_moderator[guild].remove(mod.id)
        data = read_json("bot_data.json")
        data[str(guild)]['moderator'] = self.client.guild_moderator[guild]
        write_json(data,"bot_data.json")

        await cxt.send(f"Removed {mod.name} from moderator")
        await cxt.message.delete()




    @commands.command(name="ban_channel",aliases=["no","stop","ban"])
    async def blacklist(self,cxt,channel : discord.TextChannel,state='false'):
        guild = cxt.guild.id


        # __ creating modification in blacklist __
        if state.lower() in ['true',True,"yes",'ban','t']:
            if (channel.id in self.client.blacklisted_channels[guild]):
                await cxt.send(f"Channel <#{channel.id}> is already blacklisted.")
                return
            self.client.blacklisted_channels[guild].append(channel.id)

            over_writes = channel.overwrites_for(cxt.guild.default_role)
            over_writes.send_messages = False

            over_writes_me = channel.overwrites_for(self.client.user)
            over_writes_me.send_messages = True

            await channel.set_permissions(self.client.user, overwrite=over_writes_me)
            await channel.set_permissions(cxt.guild.default_role, overwrite=over_writes,
            reason= f"Channel blacklisted by {cxt.author.nick}")#send_messages=False)

            msg = await cxt.send(f"Channel <#{channel.id}> has been blacklisted for **any message**.")
            await msg.add_reaction(emoji="✅")
        else:
            try:
                self.client.blacklisted_channels[guild].remove(channel.id)

            except ValueError:
                pass
            finally:

                over_writes = channel.overwrites_for(cxt.guild.default_role)
                over_writes.send_messages = None

                over_writes_me = channel.overwrites_for(self.client.user)
                over_writes_me.send_messages = None

                await channel.set_permissions(self.client.user, overwrite=over_writes_me)
                await channel.set_permissions(cxt.guild.default_role, overwrite=over_writes,
                    reason= f"Channel removed from blacklist by {cxt.author.nick}")
                msg = await cxt.send(f"Channel <#{channel.id}> removed from blacklist.")

        await cxt.message.delete()
        data = read_json("bot_data.json")
        data[str(guild)]['blacklisted_channels'] = self.client.blacklisted_channels[guild]
        write_json(data,"bot_data.json")


    @commands.command(name="blacklist",aliases=['bl'])
    async def blacklist_fetch(self,cxt):
        guild = cxt.guild.id
        data = read_json("bot_data.json")[str(guild)]['blacklisted_channels']
        if not data:data = "No blacklisted channels"
        else:data = ''.join([f"<#{i}>"+"\n" for i in data])
        text = discord.Embed(
            title="Blacklisted channels",
            description=data,
            colour = 65535
            )
        text.set_author(name = self.client.user.name,
            icon_url = self.client.user.avatar_url)
        await cxt.send(embed=text)

    @commands.command(name="modlist",aliases=['ml'])
    async def modlist_fetch(self,cxt):
        guild = cxt.guild.id
        data = read_json("bot_data.json")[str(guild)]['moderator']
        if not data:data = "No moderator found!"
        else:data = ''.join([f"<@{i}>"+"\n" for i in data])
        text = discord.Embed(
            title="Bot Managers for this server",
            description=data,
            colour = 65535
            )
        text.set_author(name = self.client.user.name,
            icon_url = self.client.user.avatar_url)
        await cxt.send(embed=text)

    @commands.command(name="activitylist",aliases=['al','tracklist'])
    async def activity_fetch(self,cxt):
        guild = cxt.guild.id
        data = read_json("bot_data.json")[str(guild)]['activity']
        if not data:data = "No activity channel found!"
        else:data = f"<#{data}>"
        text = discord.Embed(
            title="User Activity Channel for this server",
            description=data,
            colour = 65535
            )
        text.set_author(name = self.client.user.name,
            icon_url = self.client.user.avatar_url)
        await cxt.send(embed=text)

    @commands.command(name="ignore",aliases=["ig"])
    async def ignore(self, cxt, channel : discord.TextChannel, state = "false"):
        guild = cxt.guild.id

        if state.lower() in ['true',True,"yes",'ig','t']:
            if (channel.id in self.client.blacklisted_channels[guild]):
                await cxt.send(f"Channel <#{channel.id}> is already ignored.")
                return
            try:
                self.client.ignored_channels[guild].append(channel.id)
            except KeyError:
                self.client.ignored_channels[guild] = [channel.id]
            except AttributeError:
                self.client.ignored_channels = {guild: [channel.id] }
            cxt.send("Ignoring commands in channel <#{channel.id}> (except for bot managers)")

        else:
            try:
                self.client.ignored_channels[guild].remove(channel.id)
            except ValueError:
                pass
            finally:
                cxt.send("Removed channel <#{channel.id}> from ignore")

        await cxt.message.delete()
        data = read_json("bot_data.json")
        data[str(guild)]['ignored_channels'] = self.client.ignored_channels[guild]
        write_json(data,"bot_data.json")
    
    @commands.command(name="ignorelist", aliases=["iglist"])
    async def ignorelist(self, ctx):
        guild = ctx.guild.id
        data = read_json("bot_data.json")[str(guild)]['ignored_channels']
        if not data:data = "No ignored channel found!"
        else:data = ''.join([f"<#{i}>"+"\n" for i in data])
        text = discord.Embed(
            title="Ignored channels",
            description=data,
            colour = 65535
            )
        text.set_author(name = self.client.user.name,
            icon_url = self.client.user.avatar_url)
        await ctx.send(embed=text)


def setup(client):
    client.add_cog(Management(client))