import discord
import random
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

client = discord.Client(intents=discord.Intents.all())
token = os.getenv("DISCORD_TOKEN")

user = "ac-ulan-serveri"

global proc

def start_server():
  global proc
  proc = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_command(cmd):
  proc.stdin.write(b"" + cmd + "\n")
  proc.stdin.flush()
  print(proc.stdout.readline())

def stop_server():
  proc.stdin.close()
  proc.terminate()
  proc.wait(timeout=0.3)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if len(msg) <= 4 or msg[0:4] != "!sg ":
    return

  msg = msg[4:len(msg)]

  response = ""

  if msg == "start":
    response = "starting"
    start_server()

  if msg == "stop":
    response = "stopping"
    stop_server()

  await message.channel.send(response)

client.run(token)