import discord
from discord import FFmpegPCMAudio
import dotenv
import os
import platform

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
client = discord.Client(intents=intents)

## Detect when user enters vc ## 
@client.event
async def on_voice_state_update(member, before, after):
    # print(member.display_name)
    microwaveChannelName = 'microwave'
    if member == client.user:
        return
    
    try:
        if after.channel != None and after.channel.name == microwaveChannelName:
            # print(f'{member.display_name} has joined {after.channel.name}')
            await client.change_presence(status=discord.Status.online)
            await after.channel.connect(timeout=30, reconnect=True)
            botVC = after.channel.guild.voice_client
            if platform.system() == 'Darwin':
                discord.opus.load_opus('/opt/homebrew/Cellar/opus/1.5.1/lib/libopus.0.dylib')
            elif platform.system() == 'Linux':
                discord.opus.load_opus('libopus.so.0')
                
            def playMicrowaveSound(error):
                if error:
                    print(f'Error in playMicrowaveSound: {error}')
                elif botVC.is_connected():
                    botVC.play(FFmpegPCMAudio('Microwave Sound Effect.mp3'), after=playMicrowaveSound)
            
            botVC.play(FFmpegPCMAudio('Microwave Sound Effect.mp3'), after=playMicrowaveSound)


        if before.channel != None and before.channel.name == microwaveChannelName and before.channel.members == [client.user]:
            # print('Disconnecting')
            botVC = before.channel.guild.voice_client
            botVC.stop()
            await botVC.disconnect()
            await client.change_presence(status=discord.Status.invisible)

        
            
    except AttributeError as e:
        raise e
    #     # print(f'{member.display_name} disconnected')
    #     pass

        
 
## Run Discord Client ##
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.invisible)
    print("Ready")

client.run(TOKEN)

