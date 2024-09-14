import subprocess
import jardownloader
import os
import pwd

def all():
    print("exec")

def crUser():
  print("You need root permission to create an user:")
  # Check for root privileges before attempting creation
  if os.geteuid() == 0:
      # Use pwd.getpwnam to check if user exists
      if not pwd.getpwnam("minecraft"):
          # Use os.makedirs to create directories with proper permissions
          os.makedirs("/opt/minecraft", mode=0o750, exist_ok=True)
          # Use pwd.addUser with desired options
          pwd.addUser("minecraft", shell="/bin/bash", homedir="/opt/minecraft")
      else:
          print("User 'minecraft' already exists.")
  else:
      print("Please run as root.")

def crFolders():
    subprocess.run("sudo su minecraft -c 'mkdir -p ~/{backups,tools,server}'", shell=True)

def mcrcon():
    print('Go to https://github.com/Tiiffi/mcrcon/releases/ and download the latest version compatible with your sistem. Unzip the .tar.gz with the command tar -xvzf (filename). Copy the mcrcon file into /opt/minecraft/tools, and make it executable with chmod +x mcrcon.')
    
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
