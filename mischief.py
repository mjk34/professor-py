
async def dc (ctx, victim, client):
    filler = ['<', '>', '!', '@']

    giver_id = ctx.author.id
    victim_id = victim
    for ch in filler:
        victim_id = victim_id.replace(ch, '')
    victim_id = int(victim_id)
    victim_object = await client.fetch_user(victim_id)

    print(ctx.author.voice)
    #print(victim_object.voice.channel)
    await ctx.author.voice.self_mute('True')
    return

    if victim_object.author.voice.channel is None:
        await ctx.send(f'The user is not in a voice channel')
    else:
        await victim.voice_client.disconnect()

    return