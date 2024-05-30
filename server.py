import discord
import random
from dotenv import load_dotenv
import os
import subprocess
import threading
import time

load_dotenv()

client = discord.Client(intents=discord.Intents.all())
token = os.getenv("DISCORD_TOKEN")

user = "ac-ulan-serveri"

def output_reader(procc):
  for line in iter(proc.stdout.readline, b''):
    print('got line: {0}'.format(line.decode('utf-8')), end='')

global proc

def start_server():
  global proc
  proc = subprocess.Popen(["java", "-Xmx15G", "-Xms10G", "-jar", "mc2/fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar", "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  t = threading.Thread(target=output_reader, args=(proc,))
  t.start()
  time.sleep(20)
  proc.terminate()
  try:
    proc.wait(timeout=0.2)
    print('== subprocess exited with rc =', proc.returncode)
  except subprocess.TimeoutExpired:
    print('subprocess did not terminate in time')
  t.join()
  # java -Xms10G -Xmx15G -jar fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar nogui

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

  if msg[0:3] == "run":
    msg = msg[4:len(msg)]
    response = "running " + msg

  await message.channel.send(response)

client.run(token)
