import discord, os, udata
from discord.ui import View, Button

import mining, taxes, random

intents = discord.Intents.default()
intents.message_content = True  # Needed for slash commands
intents.members = True

bot = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(bot)

guildID = 856733214659051520


class MyView(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update button text or perform actions on click

        userid = interaction.user.id
        udata.changebal(userid, 10)

        button.label = "Clicked!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Added 10 to your balance. Your new balance is {udata.getbal(userid)}!", ephemeral=True)


@tree.command(name="bal", description="Find your own 3er3coin balance!", guild=discord.Object(id=guildID))
async def bal(interaction: discord.Interaction):
    userid = interaction.user.id

    try:
        currentbal = udata.getbal(userid)
    except:
        udata.setbal(userid, 100)
        currentbal = 100

    view = MyView()
    await interaction.response.send_message(f"Thanks user {interaction.user.name}! Your current balance is {currentbal} 3er3coin.", view=view)


@tree.command(name="lb", description="View the 3er3coin leaderboard!", guild=discord.Object(id=guildID))
async def lb(interaction: discord.Interaction):
    userdata = udata.getuserdata()
    sorted_lb = sorted(userdata.items(), key=lambda item: item[1], reverse=True)

    out_text = ""
    for entry in sorted_lb:
        uid, ubal = entry
        uname = interaction.guild.get_member(int(uid))
        out_text += f"{uname} has {ubal} 3er3coin!"
        out_text += "\n"

    await interaction.response.send_message(out_text)


@tree.command(name="set_bal", description="Change a person's 3er3coin balance!", guild=discord.Object(id=guildID))
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


@tree.command(name="mine", description="Mine for 3er3!", guild=discord.Object(id=guildID))
async def set_bal(interaction: discord.Interaction):
    code = random.randint(1000, 9999)
    print("Generating coded audio...")
    await interaction.response.send_message("Generating coded audio...")
    mining.generate_final_audio(code)
    print("Coded audio completed. Sending...")

    await interaction.followup.send(file=discord.File("output_audio.mp3"))


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildID))
    print("Enabled!!!")
    print(f'We have logged in as {bot.user}')

bot.run(os.getenv("TOKEN"))
