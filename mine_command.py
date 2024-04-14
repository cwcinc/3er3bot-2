import discord, random, datetime, mining, time, udata, asyncio
from discord.ext import commands


async def mine(bot: discord.Client, ctx: commands.Context):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    target_voice_channel_id = 1228584011212001311
    voice_channel = bot.get_channel(target_voice_channel_id)

    if ctx.author.voice is None:
        await ctx.send(f"You need to be in {voice_channel.mention} to start mining!",
                                                ephemeral=True)
        return

    if voice_client is None:
        voice_client = await voice_channel.join()
    else:
        await voice_client.connect()

    # Checking if the bot is already playing something
    if voice_client.is_playing():
        await ctx.send("Someone is already mining!", ephemeral=True)
        return

    code = random.randint(1000, 9999)
    print(f"User {ctx.author.name} has started mining. The code is {code}.")
    print("Generating coded audio...")
    await ctx.send("You slowly descend into the mines...", ephemeral=False)
    splice_time = mining.generate_final_audio(code)
    print("Coded audio completed. Playing...")
    print(
        f"Predicted to play code at {datetime.datetime.fromtimestamp(time.time() + splice_time / 1000).strftime('%H:%M:%S')}")
    # await interaction.followup.send("Here's your challenge. Good luck mining!", file=discord.File("miningChallenge.mp3"))

    if voice_client is None:
        voice_client = await voice_channel.join()
    else:
        await voice_client.connect()

    audio_source = discord.FFmpegPCMAudio("miningChallenge.mp3")
    await ctx.send("You hear the sounds of the underworld. "
                                    "Who knows what secrets might lie within!\n"
                                    "- Goal: Listen for a 4 digit passcode, "
                                    "and type it in this channel to receive your reward.", ephemeral=False)
    voice_client.play(audio_source)

    user_waiting = ctx.author.id
    waiting_channel = ctx.channel

    def check_for_reply(message):
        return message.author.id == user_waiting and message.channel == waiting_channel and message.content.isnumeric()

    try:
        reply = await bot.wait_for('message', check=check_for_reply, timeout=42 * 60)  # timeout for 42 minutes
        user_response = reply.content

        correct_code = str(user_response).strip() == str(code)
        if correct_code:
            win_percent = random.randint(1, 10)
            win_value = udata.bank_transaction(reply.author.id, win_percent)
            await reply.reply(
                f"You have escaped the mines unscathed, and successfully collected {win_value} Ʒerʒ! ({win_percent}% of Bank)")
        else:
            await reply.reply(f"Whoops, you just wasted a good portion of your life. The code was {code}")
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to respond. The code was {code}")
    finally:
        voice_client.stop()
        await voice_client.disconnect(force=False)
