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

running = False

def output_reader(procc):
  for line in iter(proc.stdout.readline, b''):
    print('got line: {0}'.format(line.decode('utf-8')), end='')

global proc
global t

def start_server():
  global running
  running = True
  global proc
  proc = subprocess.Popen(["java", "-Xmx15G", "-Xms10G", "-jar", "fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar", "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  global t
  t = threading.Thread(target=output_reader, args=(proc,))
  t.start()
  # java -Xms10G -Xmx15G -jar fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar nogui

def run_command(cmd):
  cmd += "\n"
  proc.stdin.write(cmd.encode())
  proc.stdin.flush()
  # time.sleep(1)
  # print(proc.stdout.readline())
  # time.sleep(1)

def stop_server():
  global running
  running = False
  proc.stdin.write(b"stop\n")
  proc.stdin.flush()
  proc.stdin.close()
  proc.terminate()
  try:
    proc.wait(timeout=4)
    print('== subprocess exited with rc =', proc.returncode)
  except subprocess.TimeoutExpired:
    print('subprocess did not terminate in time')
  global t
  t.join()
  proc.wait(timeout=0.3)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global running
  if message.author == client.user:
    return
  
  msg = message.content

  if len(msg) <= 4 or msg[0:4] != "!sg ":
    return

  msg = msg[4:len(msg)]

  response = ""

  if msg == "help":
    response = """start the server using '!sg start', stop the server using '!sg stop', run any command using '!sg run COMMAND', use '!sg help' for this help message"""

  if msg == "start":
    if running:
      response = "the server is already running"
    else:
      response = "starting"
      start_server()

  if msg == "stop":
    if not running:
      response = "the server is already not running"
    else:
      response = "stopping"
      stop_server()

  if msg[0:3] == "run":
    if not running:
      response = "the server is not running, so i cannot execute the command"
    else:
      msg = msg[4:len(msg)]
      response = "running " + msg
      run_command(msg)

  await message.channel.send(response)

client.run(token)
