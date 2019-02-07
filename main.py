import discord
import asyncio
import TOKEN
import pickle
import importer
import datetime
from send import Command
from commands.background import * 


loop = asyncio.get_event_loop()

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_command = []
        self.get_all_commands()
        self.loop = asyncio.get_event_loop()

        self.bg_task = self.loop.create_task(change_activity(self)) 
        print(self.load_command , "\n\n")
        self.set_black()

    def set_black(self):
        self.blacklist = []
        with open('blacklist.pickle','rb') as f:
            self.blacklist = pickle.load(f)
    
    def get_all_commands(self):
        for i in Command.commands:
            self.load_command.append(i(self))



    async def on_ready(self):
        print(self.user.name + "으로 봇이 로그인함.")
        print("=======")
        print("작동 시작!")
        print("\n\n")

    
    async def on_message(self, message):



        
        if message.author.id == 289729741387202560:



            if message.content.startswith("봇 블랙추가"):
                a = message.content
                a = a[7:]
                a = a.replace("<", "")
                a = a.replace("@", "")
                a = a.replace("!", "")
                a = a.replace(">", "")
                if a == "":
                    await message.channel.send("사용자가 선택되지 않았습니다.")
                else:
                    
                    self.blacklist.append(a)
                    thefile = open('blacklist.pickle', mode='w+')
                    thefile.write("")
                    thefile.close
                    try:
                        with open('blacklist.pickle','ab') as f:
                            pickle.dump(self.blacklist,f)
                    except:
                        pass

                    await message.channel.send("<@%s>가 블랙리스트에 추가됨..." %a)
            
            if message.content.startswith("봇 블랙초기화"):
                f = open("blacklist.pickle", mode="w+")
                f.write("")
                f.close()
                self.blacklist = []
                try:
                    with open('blacklist.pickle','ab') as f:
                        pickle.dump(self.blacklist, f)
                except:
                    pass

                await message.channel.send("블랙리스트 삭제 완료.")


            if message.content.startswith("봇 블랙삭제"):
                a = message.content
                a = a[7:]
                a = a.replace("<", "")
                a = a.replace("@", "")
                a = a.replace("!", "")
                a = a.replace(">", "")
                self.blacklist.remove(a)
                f = open("blacklist.pickle", mode="w+")
                f.write("")
                f.close()
                try:
                    with open('blacklist.pickle','ab') as f:
                        pickle.dump(self.blacklist, f)
                except:
                    pass
                
                await message.channel.send("/".join(self.blacklist))

            if message.content.startswith("봇 블랙보기"):
    
                await message.channel.send("블랙리스트 목록 : %s" %self.blacklist)

        nowtime1 = datetime.datetime.now()
        try:
            servername = message.guild.name
            serverid = message.guild.id
            channelid = message.channel.id
            channelname = message.channel.name

        except:
            channelid = "DM이라 기록되지 않았습니다."
            channelname = "DM이라 기록되지 않았습니다."
            servername = "DM이라 기록되지 않았습니다."
            serverid = "DM이라 기록되지 않았습니다."
        
        if not message.attachments == []: # 보낸 메시지에 파일이 아무것도 없으면,
            attachedfile = message.attachments[0] # 첨부파일 정보를 받아온다. ( 정보는 다음과 같이 표시됨. [{'width': 1366, 'url': 'https://cdn.discordapp.com/attachments/397039361792802816/397726279668989963/unknown.png', 'size': 222618, 'proxy_url': 'https://media.discordapp.net/attachments/397039361792802816/397726279668989963/unknown.png', 'id': '397726279668989963', 'height': 768, 'filename': 'unknown.png'}] )
            filelink = attachedfile.url # 저 데이터중 파일 url을 분석
            attach = filelink
        else:
            attach = "None"
        
        print("%s + Message Helper\n       User: %s [ %s ]\n        Server: %s [ %s ]\n       Channel: %s [ %s ]\n        Message: %s\n        File: %s\n        Embed: %s\n" %(nowtime1,message.author, message.author.id, servername, serverid, channelname, channelid, message.content,attach,message.embeds)) 


        if message.author.bot:
            return

        if str(message.author.id) in self.blacklist:
            return 
            
        for i in self.load_command:
            self.loop.create_task(i._send(message))


client = Bot()
client.run(TOKEN.bot_token)