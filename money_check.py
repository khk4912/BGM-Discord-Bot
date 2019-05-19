import discord
import TOKEN

class Check(discord.Client):
    async def on_ready(self):
        print("=====")
        print("로그인 완료 !")
        print("=====")

    async def on_message(self, message):
        if message.author.id == 289729741387202560:
            if message.content.startswith("!check"):
                code = message.content[6:].lstrip()
                code = code.split()
                channel = client.get_channel(int(code[0]))
                msg = await channel.fetch_message(int(code[1]))
                if msg.embeds:
                    msg_content = msg.embeds[0].to_dict()
                else:
                    msg_content = msg.content

                embed=discord.Embed(title="✅ Debug Message", description="{}".format(msg_content),color=0x1dc73a )
                await message.channel.send(embed=embed)

client = Check()
client.run(TOKEN.bot_token)