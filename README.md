# minecraft-discord-bot

This is Python script to run on a server that hosts Minecraft to use as a Discord bot on your guild to start/stop the Minecraft server or to run a server command.

# Installation

Download the repository using the following command in the same folder as the Minecraft server jar file.
```
git clone https://github.com/mkutay/minecraft-discord-bot
```
Then, copy the contents of the repository into the folder.
```
cp -r minecraft-discord-bot/* .
```
Run the following commands to create a virtual environment and to install the Python libraries.
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
Finally, change the following line in `server.py` according to how the Minecraft server is going to start.
```py
proc = subprocess.Popen(["java", "-Xmx15G", "-Xms10G", "-jar", "fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar", "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
```
Namely, change `-Xmx15G` as the maximum allocated memory the Minecraft server will have, change `-Xms10G` as the starting memory allocated to the Minecraft server, and change `fabric-server-mc.1.20.4-loader.0.15.11-launcher.1.0.1.jar` as the jar file that your Minecraft server will run from.

# Usage

First, a Discord bot is needed, and the token of the bot should be copied and placed in the same folder in the `.env` file (should be created first) as the following, where `XXXXX.XX.XXXXX` should be replaced with your bot's token.
```env
DISCORD_TOKEN="XXXXX.XX.XXXXX"
```
Then, the bot can be started using the following command.
```
python3 server.py
```
After adding the bot to your Discord guild, you can run `!sg start`, `!sg stop`, `!sg run COMMAND`, and `!sg help` in any channel.

# Detaching the session

To close your ssh connection and to make the bot fully detached and run in the background, `screen` can be used. Install it using any package manager, like the following.
```
sudo apt install screen
```
Then, stop the current running command, and start screen by typing `screen` to the command line. After that, start the bot normally. Now, you can detach from the session using `Ctrl + A + D`.

You can reattach to the command line using `screen -list` to list the current detached sessions, which will give an output similar to the following.
```
There is a screen on:
        25798.pts-0.vmi1905096  (05/30/2024 06:11:53 PM)        (Attached)
1 Socket in /run/screen/S-server
```
By running the command `screen -r 25798`, where `25798` is the number you get from the list, you can reattach to the session that is running the bot.

# Disclaimer

Use this Python script at your own discretion. I take no responsibility if anything should happen to your machine or Minecraft world while trying to install, test or otherwise use this software in any form.
