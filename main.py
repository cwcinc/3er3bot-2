"""
https://discord.com/api/oauth2/authorize?client_id=1227827763084529766&permissions=26795494862656&scope=bot%20applications.commands
"""

import asyncio
import time
import datetime

import discord
import os

import mine_command
import udata
from discord.ui import View

import mining
import random
import taxes

intents = discord.Intents.all()

bot = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(bot)

guildIDL = [1228578874439241728, 856733214659051520]
guildIDs = [discord.Object(i) for i in guildIDL]


@tree.command(name="bal", description="Find your own ƷerʒCoin balance!", guilds=guildIDs)
async def bal(interaction: discord.Interaction):
    userid = interaction.user.id

    try:
        currentbal = udata.getbal(userid)
    except:
        udata.setbal(userid, 0)
        currentbal = 0

    await interaction.response.send_message(f"{interaction.user.name}, your current balance is {currentbal} ƷerʒCoin.")


@tree.command(name="lb", description="View the ƷerʒCoin leaderboard!", guilds=guildIDs)
async def lb(interaction: discord.Interaction):
    userdata = udata.getuserdata()
    sorted_lb = sorted(userdata["users"].items(), key=lambda item: item[1]["bal"], reverse=True)

    out_text = ""
    for entry in sorted_lb:
        uid, ubal = entry[0], entry[1]["bal"]
        uname = interaction.guild.get_member(int(uid))
        out_text += f"{uname} has {ubal} Ʒerʒcoin!"
        out_text += "\n"
    out_text += f"**The bank has {userdata['BANK']} Ʒerʒcoin.**"

    await interaction.response.send_message(out_text)


@tree.command(name="set_bal", description="Change a person's Ʒerʒcoin balance!", guilds=guildIDs)
@discord.app_commands.checks.has_permissions(administrator=True)
async def set_bal(interaction: discord.Interaction, target: discord.Member, value: int):
    udata.setbal(target.id, value)
    await interaction.response.send_message(f"Set {target.mention}'s Ʒerʒcoin balance to {value}!")


class FinishMine(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = interaction.user.id

        button.label = "Armed."
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


@tree.command(name="mine", description="Mine for Ʒerʒ!", guilds=guildIDs)
async def mine(interaction: discord.Interaction):
    await mine_command.mine(bot, interaction)


class BetView(View):
    def __init__(self, bet_amount, user_list):
        super().__init__()
        self.bet_amount = bet_amount
        self.user_list = user_list

    @discord.ui.button(label="Join Bet", style=discord.ButtonStyle.blurple)
    async def join_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        userid = interaction.user.id

        user_balance = udata.getbal(userid)
        if user_balance < self.bet_amount:
            embed = discord.Embed(
                title=f"You do not have enough ƷerʒCoin to join this bet.",
                description=f"This bet requires you to put in {self.bet_amount} Ʒerʒ to join, and you only have {user_balance}",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if udata.is_betting(userid):
            embed = discord.Embed(
                title="You are already in another bet!",
                description="You can only join one bet at a time.",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.user_list.append(userid)
        embed = discord.Embed(
            title=f"You have joined the bet with {self.bet_amount} Ʒerʒ",
            description=f"You will be notified of the bet result soon.",
            color=discord.Color.green())
        udata.set_betting(userid, True)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="bet", description="Bet against your friends!", guilds=guildIDs)
async def bet(interaction: discord.Interaction, win_condition: str, bet_amount: int):
    u_bal = udata.getbal(interaction.user.id)
    if u_bal < bet_amount:
        await interaction.response.send_message("You do not have enough Ʒerʒ to create this bet."
                                          f"You tried to make a bet with {bet_amount} Ʒerʒ, but you only have {u_bal}.",
                                          ephemeral=True)
        return

    if bet_amount < 1:
        await interaction.response.send_message("You cannot place bets with negative or 0 Ʒerʒ!", ephemeral=True)
        return

    if udata.is_betting(interaction.user.id):
        await interaction.response.send_message("You can only participate in one bet at a time!", ephemeral=True)
        return

    udata.set_betting(interaction.user.id, True)
    user_list = [interaction.user.id]
    embed = discord.Embed(
        title=f"{interaction.user.name} bets {format(bet_amount, ',')} Ʒerʒ that...",
        description=f"**{win_condition}**",
        color=discord.Color.green())
    view = BetView(bet_amount, user_list)
    await interaction.response.send_message(embed=embed, view=view)
    await asyncio.sleep(10)
    await interaction.followup.send(f"Final participants: {', '.join([interaction.guild.get_member(i).name for i in user_list])}")

    for user_id in user_list:
        udata.set_betting(user_id, False)


@tree.command(name="cancel_mining", description="Cancel any active mining sessions.", guilds=guildIDs)
@discord.app_commands.checks.has_permissions(administrator=True)
async def cancel_mining(ctx):
    # Checking if the bot is in a voice channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        await ctx.response.send_message("There is currently no mining taking place!")
        return

    # Stopping the audio
    voice_client.stop()

    await ctx.response.send_message("Oh man you didn't like it :(")

    # Disconnecting from the voice channel
    await voice_client.disconnect()


@tree.command(name="give", description="Give someone your Ʒerʒ!", guilds=guildIDs)
async def give(interaction: discord.Interaction, target: discord.Member, amount: int):
    if target.id == 1227827763084529766:
        await interaction.response.send_message("You cannot give ƷerʒCoin to ƷerʒBot!", ephemeral=True)
        return

    if target.id == interaction.user.id:
        await interaction.response.send_message("You cannot give ƷerʒCoin to yourself!", ephemeral=True)
        return

    udata.try_new_user(target.id)
    user_bal = udata.getbal(interaction.user.id)
    if user_bal < amount:
        await interaction.response.send_message("You don't have enough ƷerʒCoin to complete this transaction."
                                                f"You attempted to send {amount} ƷerʒCoin, but you only have {user_bal}.",
                                                ephemeral=True)
        return

    udata.changebal(interaction.user.id, -amount)
    udata.changebal(target.id, amount)
    await interaction.response.send_message(f"{interaction.user.name} has successfully sent {target.name} {amount} ƷerʒCoin!")


@tree.command(name="delete_user", description="Delete a user from the database.", guilds=guildIDs)
@discord.app_commands.checks.has_permissions(administrator=True)
async def delete_user(interaction: discord.Interaction, target: discord.Member):
    if not udata.exists(target.id):
        await interaction.response.send_message("User does not exist in the database.", ephemeral=True)
        return
    userdata = udata.getuserdata()
    await interaction.response.send_message(f"Deleted {target.name} from the database.", ephemeral=True)


@tree.command(name="tax_all", description="Taxes all users.", guilds=guildIDs)
@discord.app_commands.checks.has_permissions(administrator=True)
async def tax_all(interaction: discord.Interaction):
    taxes.tax_all()
    await interaction.response.send_message("Taxed all users.", ephemeral=True)


@bot.event
async def on_ready():
    await tree.sync(guild=guildIDs[0])
    print(f'Bot logged in as {bot.user}')

bot.run(os.getenv("TOKEN"))
