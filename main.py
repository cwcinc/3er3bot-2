import discord, os
from discord.ui import View, Button


intents = discord.Intents.default()
intents.message_content = True  # Needed for slash commands

bot = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(bot)

guildID = 856733214659051520


class MyView(View):
    @discord.ui.button(label="Click Me!", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Update button text or perform actions on click
        button.label = "Clicked!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Button Clicked!", ephemeral=True)


@tree.command(name="bal", description="Find your own 3er3coin balance!", guild=discord.Object(id=guildID))
async def test_command(interaction: discord.Interaction):
    view = MyView()
    await interaction.response.send_message("This message has buttons!", view=view)

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildID))
    print("Enabled!!!")
    print(f'We have logged in as {bot.user}')

bot.run(os.getenv("TOKEN"))
