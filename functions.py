import subprocess
import jardownloader
import os

def all():
    print("exec")

def crUser():
    print("You need root permission to create an user:")
    subprocess.run("sudo useradd -r -m -U -d /opt/minecraft -s /bin/bash minecraft", shell=True)
    return 0

def crFolders():
    subprocess.run("sudo su minecraft -c 'mkdir -p ~/{backups,tools,server}'", shell=True)
    return 0

def mcrcon():
    print('Go to https://github.com/Tiiffi/mcrcon/releases/ and download the latest version compatible with your sistem. Unzip the .tar.gz with the command tar -xvzf (filename). Copy the mcrcon file into /opt/minecraft/tools, and make it executable with chmod +x mcrcon.')
    return 0

def download():
    print("""There are many minecraft server versions, and softwares. Which one do you want? (type in the code)
    1. Vanilla official server, developed by mojang.
    2. Bukkit, it is the original plugins platform, and is a third server party software.
    3. Spigot, an extension to bukkit, with performance optimizations, extra plugins and extra configuration options.
    4. Paper, an extension to Spigot, focused on performance, plugin compatibility is preserved.
    5. PurPur, an extension to Paper, for even more additional performance.
    6. Forge, the server distribution by the modloader Forge, can be used with vanilla clients, but not advised.
    7. Fabric, same as forge, but for the Fabric mod loader.
Note: all server software, except for vanilla is open source.""")
    chosen = input("number:")
    version = input("version (exmaple: 1.21):")
    while int(chosen) not in range(1,8): 
        chosen = input("inavlid server type. \nnumber:")
    if int(version.split('.')[1]) <= 17:
        jdkVersion = 16
    else:
        jdkVersion = 17
    print(f'You need to download open jdk {jdkVersion} and git, you can do so running one of the commands:')
    print(f"""Arch: sudo pacman -S jdk{jdkVersion}-openjdk git
Ubuntu: sudo apt instal git openjdk-{jdkVersion}-jdk-headless
Debian: sudo apt-get install git openjdk-{jdkVersion}-jdk-headless""")
    print("If you have already downloaded it, and it is saying that you still have to install, please look into switching java versions, and enable the required version.")
    print("in arch linux, install java-runtime-common and run archlinux-java set <JAVA_ENV_NAME>")
    print("make sure you are using java JDK, not JRE")
    if jardownloader.download(chosen, version, jdkVersion) == 0:
        subprocess.run('sudo cp server.jar /opt/minecraft/server', shell=True)

def configure():
    steps =["Open a terminal, tipe in 'sudo su minecraft - ', then cd ~/server, and then ls. There should be a server.jar file in the ls results. If it is not there, re run download.",
    "If it is there, run the server with the command 'java -Xmx1024M -Xms512M -jar server.jar nogui'. This should setup a few things for us.",
    "Now there should be a lot of new files, two of which are named 'server.properties' and 'eula.txt'. We will have to setup each one. Lets start with eula.txt.",
    "Run nano eula.txt. This will open the eula.txt file in the nano text editor in your pc. edit the line that says eula=false, and change it to eula=true. You can do so using the arrow keys in your keyboard, pressing ctrl + o to write, and the ctrl + x to exit.",
    "Next we have to setup server.properties. Open it using nano server.properties. Here you can configure a lot of things, read all the options and change them as you like, but make sure to know what it does before changing it. There are some options that are required to use with this script.",
    "Change enable-rcon to true, set rcon.port to 25575, and set rcon.password. Make sure it is a good one, as having this password will allow people to run commands as an administrator on your server.",
    "Done. Now to setting up the service. \nTip: if you want cracked minecraft support, disable 'online-mode'.",
    ]
    for i in steps:
        input(i)

def crService():
    mem = input("How much memory should the minecraft process use (in GB)? Tip: this should NOT be the entire memory of you system.")
    password = input("What password did you choose? (This will be enbeded into the servide to stop gracefully)")
    while int(mem) < 0:
        mem = input("How much memory should the minecraft process use (in GB)?Tip: this should NOT be the entire memory of you system.")
    service = f"""
[Unit]

Description=Minecraft Server

After=network.target

[Service]

User=minecraft

Nice=1

KillMode=none

SuccessExitStatus=0 1

ProtectHome=true

ProtectSystem=full

PrivateDevices=true

NoNewPrivileges=true

WorkingDirectory=/opt/minecraft/server

ExecStart=/usr/bin/java -Xmx{mem}G -Xms512M -jar server.jar nogui

ExecStop=/opt/minecraft/tools/mcrcon -H 127.0.0.1 -P 25575 -p {password} stop

[Install]

WantedBy=multi-user.target
"""
    with open("minecraft.service", "w") as file:
        file.write(content)
    subprocess.run(["sudo cp minecraft.service /etc/systemd/system/minecraft.service"], shell=True)
    print('Done! Now you can start minecraft with systemctl start minecraft, stop it with systemctl stop minecraft, and make it start with your pc, using systemctl (dis)enable minecraft')
    print('to see logs you can run journalctl -u minecraft.service -b')
    print('to see status, you can run systemctl status minecraft')
    print('and lastly, to run commands, you can use mcrcon. Look into installing it system-wide, but for now you can just run /opt/minecraft/mcrcon -H 127.0.0.1 -P 25575 -p (password). 127.0.0.1 should be switched with your servers ip addres if running from another pc.')
    return 0

def firewall():
    steps = ["To setup the firewall, look into your distros wiki, but the specific settings for minecraft, are 25565 allow tcp and udp, and 25575 allow tcp and udp. You may want to allow 22 for ssh, or 445 for samba, but make sure that you know what you are doing."]

    for i in steps:
        input(i)
    return 0


def postInstall():
    print("""
Here is how to run your server:
start: systemctl start minecraft
stop: systemctl stop minecraft
enable: systemctl enable minecraft. Starts minecraft automatically with pc
disable: systemctl disable minecraft. Stops minecraft from starting with pc
logs: you can see previous logs in /opt/minecraft/server/logs. To see current logs, run journalctl -u minecraft.service -b
console: to run console commands, run /opt/minecraft/tools/mcrcon -H (host) -P (port) -p (password) [command]. Host is the servers ip (127.0.0.1 if its your local machine), port is the port which you setup, 25575 by default, and command is the command the server should run, you can keep that empty to run multiple commands.
if you install mcrcon system-wide, you can remove the /opt/minecraft/tools from the start of the command.
backup: to backup your world, run sudo mkdir /opt/minecraft/server/backups (creates backups folder, first time only), then cp /opt/minecraft/server/world /opt/minecraft/server/backups/(backup name)/. This won't compress it at all, and it will be acessible as a normal minecraft world.
backing it up to other machines, cloud or otherwise, is also a good idea, but for that you are on your own.
""")

def autoBackup():
    print("So you want to setup auto backups? Let's go!")
    print("First make sure you have cron installed. You can do so by running crond, if it says it cant open a file, that is good. If it says that crond is not a file or directory, that means you have to install it.")
    print("Ok, now lets create a bash script to be run periodically. Go to /opt/minecraft/tools and create a backup.sh file.")
    print("inside it, write the following lines:")
    print("""
systemctl stop minecraft
mkdir /opt/minecraft/server/backup/$(date)
cp /opt/minecraft/server/level /opt/minecraft/server/backup/$(date)
systemctl start minecraft
    """)
    print("this will stop and restart the server, as without doing that, some chunks may be saved badly.")
    print("now use chmod +x backup.sh to make it executable.")
    input("press enter when you  have done the instructions above.")
    print("""
Ok, now lets create a cronjob, to do that, simply copy the backup.sh file into /etc/crond.daily, and make sure it is executeable.""")