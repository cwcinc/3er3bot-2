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

intents = discord.Intents.all()

bot = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(bot)

guildIDL = [1228578874439241728, 856733214659051520]
guildIDs = [discord.Object(i) for i in guildIDL]

class MyView(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = interaction.user.id
        udata.changebal(userid, 10)

        button.label = "Clicked!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


class MineView(View):
    @discord.ui.button(label="Go Mining!", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = "OFF TO THE MINES!"
        button.style = discord.ButtonStyle.danger
        await mine()


@tree.command(name="bal", description="Find your own 3er3coin balance!", guilds=guildIDs)
async def bal(interaction: discord.Interaction):
    userid = interaction.user.id

    try:
        currentbal = udata.getbal(userid)
    except:
        udata.setbal(userid, 0)
        currentbal = 0

    view = MineView()
    await interaction.response.send_message(f"{interaction.user.name}, your current balance is {currentbal} 3er3coin.", view=view)


@tree.command(name="lb", description="View the 3er3coin leaderboard!", guilds=guildIDs)
async def lb(interaction: discord.Interaction):
    userdata = udata.getuserdata()
    sorted_lb = sorted(userdata["users"].items(), key=lambda item: item[1], reverse=True)

    out_text = ""
    for entry in sorted_lb:
        uid, ubal = entry
        uname = interaction.guild.get_member(int(uid))
        out_text += f"{uname} has {ubal} 3er3coin!"
        out_text += "\n"
    out_text += f"**The bank has {userdata['BANK']} 3er3coin.**"

    await interaction.response.send_message(out_text)


@tree.command(name="set_bal", description="Change a person's 3er3coin balance!", guilds=guildIDs)
@discord.app_commands.checks.has_permissions(administrator=True)
async def set_bal(interaction: discord.Interaction, target: discord.Member, value: int):

    udata.setbal(target.id, value)

    await interaction.response.send_message(f"Set {target.mention}'s 3er3coin balance to {value}!")


class FinishMine(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.red)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = interaction.user.id

        button.label = "Armed."
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


@tree.command(name="mine", description="Mine for 3er3!", guilds=guildIDs)
async def mine(interaction: discord.Interaction):
    await mine_command.mine(bot, interaction)


@tree.command(name="bet", description="Bet against your friends!", guilds=guildIDs)
async def bet(interaction: discord.Interaction):
    user_list = []
    try:
        # Send the message and wait for the message object
        await interaction.response.send_message("aight")
        message = await interaction.followup.send("React to this message to bet!")

        # Add the reaction after the message is successfully sent
        await message.add_reaction("💰")
    except discord.HTTPException as e:
        # Handle errors if the message fails to send
        await interaction.response.send_message(f"An error occurred: {e}")

    def check(reaction_type, the_user):
        return the_user != bot.user and str(reaction_type.emoji) == "💰"

    reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)
    user_list.append(user.id)

    await asyncio.sleep(30)
    await interaction.followup.send(f"The users who reacted are {user_list}")


@tree.command(name="stop", description="Stop audio", guilds=guildIDs)
async def stop(ctx):
    # Checking if the bot is in a voice channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        await ctx.response.send_message("I'm not in a voice channel!")
        return

    # Stopping the audio
    voice_client.stop()

    await ctx.response.send_message("Oh man you didn't like it :(")

    # Disconnecting from the voice channel
    await voice_client.disconnect()


@bot.event
async def on_ready():
    await tree.sync(guild=guildIDs[0])
    print(f'Bot logged in as {bot.user}')

bot.run(os.getenv("TOKEN"))
