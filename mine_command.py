import discord, random, datetime, mining, time, udata, asyncio, functools


async def run_blocking(client, blocking_func, *args, **kwargs):
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)


async def mine(bot: discord.Client, interaction: discord.Interaction):
    voice_client = discord.utils.get(bot.voice_clients, guild=interaction.guild)
    target_voice_channel_id = 1228584011212001311
    voice_channel = bot.get_channel(target_voice_channel_id)

    if interaction.user.voice is None:
        await interaction.response.send_message(f"You need to be in {voice_channel.mention} to start mining!",
                                                ephemeral=True)
        return

    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)

    # Checking if the bot is already playing something
    if voice_client.is_playing():
        await interaction.response.send_message("Someone is already mining!", ephemeral=True)
        return

    code = random.randint(1000, 9999)
    print(f"User {interaction.user.name} has started mining.")
    #  print("Generating coded audio...")
    # await interaction.response.send_message("You slowly descend into the mines...", ephemeral=False)
    await interaction.response.send_message(file=discord.File("enter_the_mines.png"), silent=True, delete_after=60)

    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)

    audio_source = discord.FFmpegPCMAudio("waiting_sound.mp3")
    voice_client.play(audio_source)
    render_start_time = time.time()
    splice_time = await run_blocking(bot, mining.generate_final_audio, code)
    #  print("Coded audio completed. Playing...")

    # await interaction.followup.send("Here's your challenge. Good luck mining!", file=discord.File("miningChallenge.mp3"))

    #  await interaction.followup.send("You hear the sounds of the underworld. "
    #                                "Who knows what secrets might lie within!\n"
    #                                "- Goal: Listen for a 4 digit passcode, "
    #                                "and type it in this channel to receive your reward.", ephemeral=False)

    audio_source = discord.FFmpegPCMAudio("miningChallenge.mp3")
    voice_client.stop()
    voice_client.play(audio_source)

    start_time = time.time()
    datetime_object = datetime.datetime.fromtimestamp(start_time + splice_time / 1000)
    print(f"VC audio started. Predicted to play code ({code}) at "
          f"{(datetime_object.hour - 1)%12 + 1}{datetime_object.strftime(':%M:%S %p')}")
    print(f"Rendering took {start_time - render_start_time} seconds.")

    user_waiting = interaction.user.id
    waiting_channel = interaction.channel

    def check_for_reply(message):
        return message.channel == waiting_channel and message.content.isnumeric()  # and message.author.id == user_waiting

    try:
        reply = await bot.wait_for('message', check=check_for_reply, timeout=40 * 60)  # timeout for 40 minutes
        user_response = reply.content

        correct_code = str(user_response).strip() == str(code)
        if correct_code:
            win_percent = random.randint(1, 5)
            win_value = udata.bank_transaction(reply.author.id, win_percent)
            await reply.reply(
                f"__{reply.author.name}__ has escaped the mines and claimed their reward of **{win_value} Ʒerʒ**! (*{win_percent}%*)\n"
                f"This exploration took __{reply.author.name}__ around **{round((time.time() - start_time) / 60)} minutes**.")
        else:
            await reply.reply(f"__{interaction.user.name}__ leaves the mines with a handful of fake ƷerʒCoin, having failed their search.\n"
                              f"The code was **{code}**.")
    except asyncio.TimeoutError:
        await reply.reply(f"__{interaction.user.name}__ leaves the mines empty handed, not even attempting to claim their reward.\n"
                          f"The code was **{code}**.")
    finally:
        voice_client.stop()
        await voice_client.disconnect()
