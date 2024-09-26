from termcolor import colored
import sys
import functions

class Operation:
    def __init__(self, name, description, function):
        self.name = name
        self.description = description
        self.function = function

    def __str__(self):
        return f"{colored(self.name,'blue', attrs=['bold'])}: {self.description}"

operations = [
    Operation("all", "Execute all operations in order", lambda: all()),
    Operation("crUser", "Create the Minecraft user and set its home folder", lambda: functions.crUser()),
    Operation("crFolders", "Creates the folder structure in /opt/minecraft", lambda: functions.crFolders()),
    Operation("mcrcon", "Helper to install mcrcon", lambda: functions.mcrcon()),
    Operation("download", "Automatically downloads minecraft server.jar, and JRE", lambda: functions.download()),
    Operation("configure", "Accepts eula.txt, enables rcon and opens server.properties", lambda: functions.configure()),
    Operation("crService", "Creates the systemd service for the minecraft server, so that it starts with the system", lambda: functions.crService()),
    Operation("firewall", "Helps  you setup the firewall", lambda: functions.firewall()),
    Operation("autoBackup", "Setups a cronjob to automatically backup", lambda: functions.autoBackup()),
    Operation("postInstall", "Basic commands and usage after setup", lambda: functions.postInstall()),
    Operation("help", "Shows this list", lambda: help())
]

def help():
    print(f"""Usage:
{colored('python main.py [operation]', attrs=['bold'])}

Operations:
{'\n'.join(str(op) for op in operations)}""")

def all():
    pad = 12
    for op in operations:
        if not op.name == 'all':
            jump = pad - len(op.name)
            print(f" {colored('------------------', attrs=['bold'])} {colored('Now running: ', 'blue')} {op.name} {' ' * jump} {colored('--------------------------------', attrs=['bold'])}")
            op.function()
            a = input("Enter to continue, c to cancel: ")
            if a == "c":
                exit()

if len(sys.argv) > 1:
    operation_name = sys.argv[1]
    for op in operations:
        if op.name == operation_name:
            op.function()
            break
    else:
        print(f"Invalid operation: {operation_name}")
        print("Use 'help' for a list of valid operations.")
else:
    help()

