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
    Operation("all", "Execute all operations in order", lambda: functions.all()),
    Operation("crUser", "Create the Minecraft user and set its home folder", lambda: functions.crUser()),
    Operation("crFolders", "Creates the folder structure in /opt/minecraft", lambda: functions.crFolders()),
    Operation("mcrcon", "Helper to install mcrcon", lambda: functions.mcrcon()),
    Operation("download", "Automatically downloads minecraft server.jar, and JRE", lambda: functions.download()),
    Operation("configure", "Accepts eula.txt, enables rcon and opens server.properties", lambda: functions.configure()),
    Operation("crService", "Creates the systemd service for the minecraft server, so that it starts with the system", lambda: functions.crService()),
    Operation("firewall", "Helps  you setup the firewall", lambda: functions.firewall()),
    Operation("start", "Starts the minecraft server", lambda: functions.start()),
    Operation("enable", "Enables the service (so that it starts with the system)", lambda: functions.enable()),
    Operation("disable", "Disables the seriver (so that is doesn't start with the sistem)", lambda: functions.disable()),
    Operation("backup", "Creates a backup of the world", lambda: functions.backup()),
    Operation("autoBackup", "Setups a cronjob to automatically backup", lambda: functions.autoBackup()),
    Operation("logs", "Shows server logs", lambda: functions.logs()),
    Operation("console", "Allows to run server commands", lambda: functions.console()),
    Operation("help", "Shows this list", lambda: help())
]

def help():
    print(f"""Usage:
{colored('python main.py [operation]', attrs=['bold'])}

Operations:
{'\n'.join(str(op) for op in operations)}""")

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

