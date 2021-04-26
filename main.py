import discord
from tinydb import TinyDB, Query, where
from tinydb.operations import delete
import uuid, time, os, asyncio

tododb = TinyDB('tododb.json')

client = discord.Client()

startTime = time.time()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    while True:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="it help를"))
      await asyncio.sleep(10)
      #Create a variable that contains all the servers
      activeServers = client.guilds
      #Create a variable to store amount of members per server
      sum = 0
      #Loop through the servers, get all members and add them up
      for s in activeServers:
        sum += len(s.members)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{len(client.guilds)}개의 서버에서 사용자의 할일을"))   
      await asyncio.sleep(10)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not tododb.contains(Query().maker == message.author.id):
      tododb.insert({"maker": message.author.id, 'todoname': 'Star in KOREANBOTS', 'uuid': f'{uuid.uuid4()}'})
    if message.content.startswith('it list'):
      todostr = f"{message.author.name}님의 ToDo\n\n"
      for i in range(1, len(tododb.search(Query().maker == message.author.id))):
        todostr = todostr + f"{i}. {tododb.search(Query().maker == message.author.id)[i]['todoname']} ({tododb.search(Query().maker == message.author.id)[i]['uuid']})\n"
      await message.channel.send(todostr)
    if message.content.startswith('it add '):
      if len(tododb.search(Query().maker == message.author.id)) > 30:
        await message.channel.send("ToDo가 너무 많아요! ~~개발자를 생각해서~~ 좀 해결하는것은 어떨까요?")
      tododb.insert({'maker': message.author.id, 'todoname': message.content[6:], 'uuid': f'{uuid.uuid4()}'})
      await message.channel.send("성공적으로 ToDo가 저장되었습니다. ")
    if message.content.startswith('it mark '):
      try:
        a = tododb.search(Query().uuid == message.content.split()[2])[0]
        if a['maker'] != message.author.id:
          await message.channel.send("남의 일을 대신 해주려는 마음은 좋지만, 그렇게 하면 다른 사람이 햇깔리지 않을까요?")
        else:
          tododb.remove(Query().uuid == message.content.split()[2])
          await message.channel.send("ToDo 하나를 완료하신 것을 축하합니다!")
      except TypeError:
        await message.channel.send("명령어를 잘못 사용하셨습니다. ")
    if message.content.startswith('it invite'):
      await message.channel.send("<https://discord.com/oauth2/authorize?client_id=833036716230049792&permissions=326720&scope=bot> 여기에서 이 봇을 초대하세요!\n<https://discord.gg/ZFB2wD6CUM> 여기에서 봇의 서포트 서버로 들어가세요!")
    if message.content.startswith('it ping'):
      current_time = time.time()
      pingmsg = await message.channel.send("핑 측정중...")
      msgpingtime = time.time()
      pingtime = int((msgpingtime*1000) - (current_time*1000))
      await pingmsg.delete()
      updifference = int(round(current_time - startTime))
      uptext = f"{updifference}초"
      
      embed=discord.Embed(title="봇의 상태", description=f"{client.user.mention} 에 대하여", color=0x864ffe)
      embed.add_field(name="이름", value=client.user.name, inline=True)
      embed.add_field(name="만들어진 날", value=client.user.created_at, inline=True)
      embed.add_field(name="활동중인 서버 개수", value=f"{len(client.guilds)}개", inline=True)
      #len(client.guilds)
      embed.set_thumbnail(url=client.user.avatar_url)
      embed.add_field(name="Ping", value=f"{pingtime}ms", inline=True)
      embed.add_field(name="업타임", value=uptext, inline=True)
      await message.channel.send(embed=embed)
    if message.content.startswith("it hellothisisverification"):
      await message.channel.send("injoon5#0225(741109989309153290)")  
    if message.content.startswith("ithellothisisverification"):
      await message.channel.send("제가 봇 접두사를 특이하게 지정해서... 원래는 `it hellothisisverification`입니다.\n정보는 여기있습니다: \ninjoon5#0225(741109989309153290)")  
    if message.content.startswith("it help"):
      guild = str(message.guild)
      #### Create the initial embed object ####
      embed1=discord.Embed(title="Ij5-ToDo help", description="Ij5-ToDo의 도움말 입니다. 여기서 명령어에 대해 알아보세요!", color=discord.Color.blue())
      embed1.add_field(name="`it list`", value="자신의 ToDo를 모두 보여준다. ", inline=True) 
      embed1.add_field(name="`it add (ToDo 이름)`", value="(ToDo 이름)으로 ToDo를 생성한다. ", inline=True)
      embed1.add_field(name="`it mark (it list 를 사용하면 뒤에 붙는 이상한 문자)`", value="입력한 문자에 해당하는 ToDo를 완료로 표시하고 지운다. ", inline=True)
      embed1.add_field(name="`it ping`", value="ping 과 봇에 관련된 각종 정보 확인", inline=True)
      embed1.set_footer(text=f"{guild}에서 이 봇을 사용해 주셔서 감사합니다. \n이 봇을 자신의 서버에 초대하거나 서포트 서버에 들어가려면?\n it invite 로 자세한 정보를 알아보세요.\nMade with ❤️ by injoon5#0225") 
      await message.channel.send(embed=embed1)

client.run(os.getenv("dctoken"))