import discord, os
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@tree.command(
    name="first",
    description="My first application Command",
    guild=discord.Object(id=856733214659051520)
)
async def first(ctx, title: str, description: str):
    embed=discord.Embed(title=title, description=description, color=discord.Color.blue())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Latin_letter_small_capital_ezh.svg/1200px-Latin_letter_small_capital_ezh.svg.png")
    await ctx.response.send_message(embed=embed, ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=856733214659051520))
    print("Enabled!!!")
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