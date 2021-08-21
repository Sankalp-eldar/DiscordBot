import discord
from discord.ext import commands
# import os
from modules import read_json,write_json


class Story(commands.Cog):

    def __init__(self,client):
        self.client = client
        # self.breaks = [".","?"]

    @commands.command(name="compile",aliases=["c"])
    @commands.has_permissions(administrator=True)
    async def compile_(self,ctx,start : discord.Message=None,send = "false",*,talk=None):
        # channel : discord.TextChannel = None,


        if not start:
            txt = ("I am not giving history of this channel\n"
                  "provide a `messageID` from where Story started.\n"
                  "Syntax: `;;compile <messageID>`")
            await ctx.send(txt)
            await ctx.message.delete()
            return
        await ctx.message.delete()

        story = ''''''#list()
        await ctx.channel.trigger_typing()
        story += (start.content)
        async for i in ctx.channel.history(limit=100_000,after=start):
            data = i.content
            if i.author.bot or data.startswith(";;"):
                continue
            story += " " + data.strip()


        story = " ".join(story)
        new_story = [story[i:i+1500] for i in range(0, len(story), 1500)]


        if send.lower() not in ["true","here","post",'t']:
            x = await ctx.send("I have DM you the story.")
            await x.delete(delay=2)
            reciver = ctx.author
        else:
            reciver = ctx.channel

        if not talk:talk = "**CURRENT STORY**\n"
        for i,story in enumerate(new_story):
            if i == 0:
                await reciver.send("**"+talk+"**\n"+story)
            else:
                await reciver.send(story)


    @commands.command(name="start",aliases=["sts"])
    @commands.has_permissions(administrator=True)
    async def start(self,ctx,*,talk="Recording story after this message:"):
        guild = ctx.guild.id
        data = read_json("bot_data.json")

        if data[str(guild)].get("story_message"):
            return await ctx.send("There is an ongoing story, end it before stating new.")
        msg = await ctx.send(talk)
        data[str(guild)]["story_message"] = msg.id
        write_json(data,"bot_data.json")
        await ctx.message.delete()

    @commands.command(name="end",aliases=["ss"])
    @commands.has_permissions(administrator=True)
    async def end(self,ctx,send="false",*,talk=None):
        guild = ctx.guild.id
        data = read_json("bot_data.json")

        msg = data[str(guild)].get("story_message")
        if not msg:
            return await ctx.send("No ongoing story found! See `;;help start`")

        message = await ctx.fetch_message(msg)
        async for i in ctx.channel.history(limit=1,after=message):
            message = i
        await self.compile_(ctx, message, send = send,talk=talk)

        del data[str(guild)]["story_message"]
        write_json(data,"bot_data.json")


def setup(client):
    client.add_cog(Story(client))