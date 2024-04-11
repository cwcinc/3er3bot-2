import discord, os
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@tree.command(
    name="first",
    description="My first application Command",
    guild=discord.Object(id=12417128931)
)
async def first(interaction):
    await interaction.response.send_message("Hello yayyy!")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=856733214659051520))
    print(f'We have logged in as {client.user}')

"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
"""

client.run(os.getenv("TOKEN"))