from mcrcon import MCRcon
import subprocess
import time
import re

def Sint(string):
    return re.sub(r"\D", "", string)

with MCRcon("localhost", "24727", 25575) as mcr:
    print("Python connected")

    while True:
        result = mcr.command("scoreboard players get difficulty random")
        mcr.command("say \"" + result+"\"")
        print(result)

        time.sleep(0.2)
        
