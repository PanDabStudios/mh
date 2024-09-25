# Minecraft server helper

This is a simple script to helo you setup your minecraft server, it will do some jobs automatically, some it will walk you through doing it.

To see usage, run python main.py help

Make sure you have all dependencies installed, with pip -r requirements.txt

## Functions:
- all -> executes all functions in order
- crUser -> creates the minecraft user, and sets its home folder to /opt/minecraft
- crFolders -> creates the folder structure in /opt/minecraft
- mcrcon -> Walks you through installing the mcrcon program, needed to run commands from the server console
- download -> downloads server software
- configure -> walks you through setting some basic options for your server.
- crService -> create a systemd service for the server
- firewall -> Helps you setup you firewall for the server
- autoBackup -> setups a cronjob to backup your servers world
- postInstall -> Quick sheet for basic usage
- help -> shows this list.

## How it works:

There are 3 .py files, each of them doing a specific task.
1. Main.py is the CLI interface, help page and "all" function.
2. Functions.py is all other functionalities, except for 
3. jardownloader.py, which interfaces with the APIs of all the minecraft server softwares to download them in the correct version. Spigot and Bukkit are even built  by it!

## Design decisions:

There are some desing decisions which im not proud of, I would much rather have it all be automaticall instead of walking through the process, but I decided that it would be easier for myself, and better for the end user, for them to actually walk through all the steps, and understand most to all of them instead of having to create another entire interface for just running it.

## 