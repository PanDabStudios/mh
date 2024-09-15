import requests
import urllib
import subprocess
import re

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'MinecraftDownloader/1.0 (https://.com/)')]
urllib.request.install_opener(opener)

def download(software, wantedVersion, jdkVersion):
    if int(software) == 6:
        print(f'because forge uses a installer, you will have to download and set it up by yourself. Here is the link: https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html')
        return 1
    elif int(software) == 1:
        url = ''
        response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json').json()
        for version in response["versions"]:
            if version['id'] == wantedVersion:
                print('found')
                url = requests.get(version['url']).json()["downloads"]["server"]["url"]
        if url == '':
            print('Invalid version ID')
            return 1
        urllib.request.urlretrieve(url, 'server.jar')
        return 0
    elif int(software) == 2 or int(software) == 3:
        print('as you need to build the server, this can take a while.')
        urllib.request.urlretrieve('https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar', 'BuildTools.jar')

        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        except FileNotFoundError:
            print("Java is not installed. Please install it and try again.")
            return 1

        match = re.search(r"openjdk version \"(\d+)\.\d+\.\d+\"", result.stderr)
        if not match:
            print("Error parsing Java version.")
            return 1
        java_version = match.group(1)
        print(java_version)

        if int(java_version) < jdkVersion:
            print(f"Java version {java_version} is too old. Please install and enable Java Development Kit (jdk) {jdkVersion} or higher.")
            return 1

        try:
            if int(software) == 2:
                subprocess.run(["java", "-jar", "BuildTools.jar", "--compile" , "craftbukkit","--rev", wantedVersion])
                subprocess.run(["cp", f"craftbukkit-{wantedVersion}.jar", "server.jar"])
            else:
                subprocess.run(["java", "-jar", "BuildTools.jar", "--final-name", "server.jar", "--rev", wantedVersion])
                subprocess.run(["cp", f"work/server-{wantedVersion}.jar", "server.jar"])
        except:
            print("there was an error compiling, see the compiling wiki, and copy the desired server.jar into /opt/minecraft/server. Make sure it is name exactly 'server.jar'.")
            print("The wiki: https://www.spigotmc.org/wiki/buildtools/#issues-and-common-concerns")
            return 1
        print("Server build completed.")
        return 0
    elif int(software) == 4:
        #Paper
        response = requests.get('https://api.papermc.io/v2/projects/paper/versions/' + wantedVersion).json()
        build = response["builds"][-1]
        if not build:
            print('Invalid version, or not yet supported by paper.')
            return 1
        url = f'https://api.papermc.io/v2/projects/paper/versions/{wantedVersion}/builds/{build}/downloads/paper-{wantedVersion}-{build}.jar'
        #print(url)
        urllib.request.urlretrieve(url, 'server.jar')
        return 0
    elif int(software) == 5:
        # purpur TODO: fix forbidden
        url = f'https://api.purpurmc.org/v2/purpur/{wantedVersion}/latest/download'
        print(url)
        urllib.request.urlretrieve(url, 'server.jar')
        return 0
    elif int(software) == 7:
        url = f'https://meta.fabricmc.net/v2/versions/loader/{wantedVersion}/0.16.5/1.0.1/server/jar'
        print(url)#                                                         Lodaer and installer versions, they don't upgrade frequently, and would add a lot of complexity
        urllib.request.urlretrieve(url, 'server.jar')
        return 0