import discord
from discord.ext import commands
# 設置意圖
# 確認 Opus 已加載
if not discord.opus.is_loaded():
    discord.opus.load_opus('/opt/homebrew/lib/libopus.dylib')  # Opus 的路徑
intents = discord.Intents.default()
intents.message_content = True  # 啟用接收訊息內容的意圖
intents.voice_states = True     # 啟用監聽語音狀態變更的意圖
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def ready_on():

    #這裡是機器人上線後預計會執行的程式
    print('目前登入身分', client.user)
    
    #也可以利用指令, 更改機器人目前在玩的遊戲
    game = discord.Game('輸入你想讓機器人顯示的狀態')
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.command()
async def join(ctx):
    
    #這裡的指令會讓機器人進入call他的人所在的語音頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.author.voice == None:
        await ctx.send("You are not connected to any voice channel")
    elif voice == None:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    else:
        await ctx.send("Already connected to a voice channel")
        
@client.command()
async def leave(ctx):
    
    #離開call他那個伺服器的所在頻道
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await ctx.send("The Bot is not connected to a voice channel")
    else:
        await voice.disconnect()
        
from pytube import YouTube
import os

def endSong(path):

    #播放完後的步驟, 進行前一首歌刪除, 抓取一首清單內的歌進行播放
    os.remove(path)
    if len(playing_list) != 0:
        voice = discord.utils.get(client.voice_clients)
        url = playing_list[0]
        del playing_list[0]
        
        YouTube(url).streams.first().download()
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                os.rename(file,"song.mp4")
        
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg/bin/ffmpeg.exe", source="song.mp4"),after = lambda x: endSong("song.mp4"))
playing_list = []

@client.command()
async def play(ctx, *, song_name: str):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    if voice is None:
        await ctx.send("我不在任何語音頻道中，請使用 !join 先加入語音頻道。")
        return
    
    if voice.is_playing():
        await ctx.send("我已經在播放音樂！")
        return

    # 本地 MP3 檔案路徑
    song_path = f"./{song_name}.mp3"
    
    if os.path.isfile(song_path):
        # 播放音樂
        voice.play(discord.FFmpegPCMAudio(executable="/opt/homebrew/bin/ffmpeg", source=song_path))

        await ctx.send(f"正在播放 {song_name}.mp3")
    else:
        await ctx.send(f"找不到檔案 {song_name}.mp3，請確保檔案存在於當前目錄。")
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing")
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not pause")
@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
client.run('MTI4OTI1ODU4MzE5MTU4NDg3OA.GATh2L.PKF07QNBr0Pdsns1nffkX0vC_hfksytc98Qa1A')
