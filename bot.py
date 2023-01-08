import discord
import json
import time
import davidbase as db

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def now():
    return time.time()
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


def getUrls(message: discord.Message):
    if message:
        return list(map(lambda att: att.url, message))
    return None

@client.event
async def on_message(message: discord.Message):
    newMessage = {
        "Message": message.content,
        "Member": message.author.name,
        "Timestamp": now(),
        "Attachments": getUrls(message.attachments),
        "Embeds": getUrls(message.embeds)
    }
    db.saveMessage(newMessage)
@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after):
    if not before.channel and after.channel:
        # print(f'{member} has joined the vc')
        vc = {
            "Member": member.name,
            "Timestamp": now(),
            "Joined": True,  # True if joined, False if left.
        }
        db.saveVC(vc)
    if before.channel and not after.channel:
        # print(f'{member} has joined the vc')
        vc = {
            "Member": member.name,
            "Timestamp": now(),
            "Joined": False,  # True if joined, False if left.
        }
        db.saveVC(vc)
        
token = ""
with open("secret.json", "r") as f:
    data = json.load(f)
    token = data['token']

client.run(token)
