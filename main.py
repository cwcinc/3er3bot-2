"""
https://discord.com/api/oauth2/authorize?client_id=1227827763084529766&permissions=26795494862656&scope=bot%20applications.commands
"""

import asyncio
import time
import datetime

import discord
from discord.ext import commands

import os

import mine_command
import udata
from discord.ui import View


description = """
I've got Ʒerʒ.
"""

intents = discord.Intents.all()

guildIDL = [1228578874439241728, 856733214659051520]
guildIDs = [discord.Object(i) for i in guildIDL]

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("Ʒ"),
    description=description,
    intents=intents,
    debug_guilds=guildIDL
)


class MyView(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = interaction.user.id
        udata.changebal(userid, 10)

        button.label = "Clicked!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


class MineView(View):
    @discord.ui.button(label="Go Mining!", style=discord.ButtonStyle.green)
    async def button_callback(self, ctx: commands.Context, button: discord.ui.Button):
        button.label = "OFF TO THE MINES!"
        button.style = discord.ButtonStyle.danger
        await mine()


@bot.command()
async def bal(ctx: commands.Context):
    """Get your balance!"""
    userid = ctx.author.id

    try:
        current_bal = udata.getbal(userid)
    except KeyError:
        udata.setbal(userid, 0)
        current_bal = 0

    view = MineView()
    await ctx.respond(f"{ctx.author.name}, your current balance is {current_bal} ƷerʒCoin.", view=view)


@bot.command()
async def lb(ctx: commands.Context):
    userdata = udata.getuserdata()
    sorted_lb = sorted(userdata["users"].items(), key=lambda item: item[1], reverse=True)

    out_text = ""
    for entry in sorted_lb:
        uid, ubal = entry
        uname = ctx.guild.get_member(int(uid))
        out_text += f"{uname} has {ubal} Ʒerʒcoin!"
        out_text += "\n"
    out_text += f"**The bank has {userdata['BANK']} Ʒerʒcoin.**"

    await ctx.send(out_text)


@bot.command(name="set_bal", description="Change a person's Ʒerʒcoin balance!", guilds=guildIDs)
@commands.has_permissions(administrator=True)
async def set_bal(ctx: commands.Context, target: discord.Member, value: int):

    udata.setbal(target.id, value)

    await ctx.send(f"Set {target.mention}'s Ʒerʒcoin balance to {value}!")


class FinishMine(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.red)
    async def button_callback(self, ctx: commands.Context, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = ctx.author.id

        button.label = "Armed."
        await ctx.message.edit_message(view=self)
        await ctx.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


@bot.command(name="mine", description="Mine for Ʒerʒ!", guilds=guildIDs)
async def mine(ctx: commands.Context):
    await mine_command.mine(bot, ctx)


class BetView(View):
    def __init__(self, bet_amount):
        super().__init__()
        self.bet_amount = bet_amount

    @discord.ui.button(label="Join Bet", style=discord.ButtonStyle.blurple)
    async def join_bet(self, ctx: commands.Context, button: discord.ui.Button):
        userid = ctx.author.id

        user_balance = udata.getbal(userid)
        if user_balance > self.bet_amount:
            pass
        embed = discord.Embed(
            title=f"You have joined the bet with {self.bet_amount} Ʒerʒ",
            description=f"Yay",
            color=discord.Color.green())

        message = await ctx.send(embed=embed, ephemeral=True)
        print(message)

        # Wait for 30 seconds
        await asyncio.sleep(5)

        # Delete the message
        await message.delete()


@bot.command(name="bet", description="Bet against your friends!", guilds=guildIDs)
async def bet(ctx: commands.Context, win_condition: str, bet_amount: int):
    user_list = []
    embed = discord.Embed(
        title=f"{ctx.author.name} bets {format(bet_amount, ',')} Ʒerʒ that...",
        description=f"**{win_condition}**",
        color=discord.Color.green())
    view = BetView(bet_amount)
    await ctx.send(embed=embed, view=view)


@bot.command(name="cancel_mining", description="Cancel any active mining sessions.", guilds=guildIDs)
async def stop(ctx):
    # Checking if the bot is in a voice channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        await ctx.send("I'm not in a voice channel!")
        return

    await ctx.send("Oh man you didn't like it :(")

    # Disconnecting from the voice channel
    await voice_client.disconnect(force=False)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

bot.run(os.getenv("TOKEN"))
